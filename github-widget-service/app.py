from flask import Flask, Response, request
import requests
from datetime import datetime
import pytz
import hashlib

app = Flask(__name__)

# Simple in-memory stats tracking
stats = {
    'total_requests': 0,
    'last_request': None,
    'requests_history': []
}

@app.route('/widget.svg')
def widget():
    """Generate time & weather widget SVG dynamically"""
    
    # Track stats
    stats['total_requests'] += 1
    stats['last_request'] = datetime.utcnow()
    stats['requests_history'].append(datetime.utcnow())
    # Keep only last 100 requests
    if len(stats['requests_history']) > 100:
        stats['requests_history'] = stats['requests_history'][-100:]
    
    # Get Barcelona time
    bcn_tz = pytz.timezone('Europe/Madrid')
    now_bcn = datetime.now(bcn_tz)
    
    # Get New York time
    ny_tz = pytz.timezone('America/New_York')
    now_ny = datetime.now(ny_tz)
    
    # Format times - no seconds since GitHub caches for ~5 minutes
    bcn_time_str = now_bcn.strftime('%H:%M')
    ny_time_str = now_ny.strftime('%H:%M')
    date_str = now_bcn.strftime('%A, %B %d, %Y')
    
    # Calculate "last updated" for display (always shows as "just now" on server side)
    update_time = now_bcn.strftime('%H:%M')
    
    # Get weather data
    try:
        weather_url = "https://wttr.in/Barcelona?format=j1"
        response = requests.get(weather_url, timeout=10)
        weather_data = response.json()
        
        current = weather_data['current_condition'][0]
        temp = current['temp_C']
        feels_like = current['FeelsLikeC']
        weather_desc = current['weatherDesc'][0]['value']
        humidity = current['humidity']
        wind_speed = current['windspeedKmph']
        wind_dir = current['winddir16Point']
        
        # Weather icon mapping
        weather_icons = {
            'Sunny': '☀️',
            'Clear': '🌙',
            'Partly cloudy': '⛅',
            'Cloudy': '☁️',
            'Overcast': '☁️',
            'Mist': '🌫️',
            'Patchy rain possible': '🌦️',
            'Light rain': '🌧️',
            'Moderate rain': '🌧️',
            'Heavy rain': '⛈️',
            'Thundery outbreaks possible': '⚡'
        }
        
        icon = '🌤️'
        for key in weather_icons:
            if key.lower() in weather_desc.lower():
                icon = weather_icons[key]
                break
                
    except Exception as e:
        temp = "??"
        weather_desc = "Loading..."
        icon = "🌤️"
        humidity = "??"
        wind_speed = "??"
        wind_dir = "?"
        feels_like = "??"
    
    # Create stunning SVG with animation
    svg = f'''<svg width="600" height="170" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0d1117;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#161b22;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="timeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#00ff00;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#00cc00;stop-opacity:1" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <!-- Pulse animation for Live indicator -->
    <style>
      @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.5; }}
      }}
      .live-indicator {{
        animation: pulse 2s ease-in-out infinite;
      }}
    </style>
  </defs>
  
  <!-- Background -->
  <rect width="600" height="170" rx="10" fill="url(#bgGrad)" stroke="#ff1493" stroke-width="3"/>
  
  <!-- Time Section -->
  <text x="20" y="28" font-family="'Courier New', monospace" font-size="12" fill="#00ff00" font-weight="bold">🏖️ BARCELONA</text>
  <text x="20" y="58" font-family="'Courier New', monospace" font-size="36" fill="url(#timeGrad)" font-weight="bold" filter="url(#glow)">{bcn_time_str}</text>
  <text x="20" y="73" font-family="'Arial', sans-serif" font-size="9" fill="#8b949e">{date_str}</text>
  
  <!-- New York Time -->
  <text x="20" y="100" font-family="'Courier New', monospace" font-size="12" fill="#58a6ff" font-weight="bold">🗽 NEW YORK</text>
  <text x="20" y="133" font-family="'Courier New', monospace" font-size="36" fill="#58a6ff" font-weight="bold">{ny_time_str}</text>
  
  <!-- Divider -->
  <line x1="300" y1="15" x2="300" y2="155" stroke="#30363d" stroke-width="2"/>
  
  <!-- Weather Section -->
  <text x="320" y="30" font-family="'Arial', sans-serif" font-size="14" fill="#00ff00" font-weight="bold">🌤️ BCN WEATHER</text>
  <text x="320" y="78" font-family="'Arial', sans-serif" font-size="42" fill="#ffffff" font-weight="bold">{icon} {temp}°C</text>
  <text x="320" y="103" font-family="'Arial', sans-serif" font-size="14" fill="#8b949e">{weather_desc}</text>
  <text x="320" y="125" font-family="'Arial', sans-serif" font-size="12" fill="#8b949e">Feels like {feels_like}°C • Humidity {humidity}%</text>
  <text x="320" y="145" font-family="'Arial', sans-serif" font-size="12" fill="#8b949e">Wind {wind_speed} km/h {wind_dir}</text>
  
  <!-- Footer with Live indicator -->
  <circle cx="220" cy="158" r="3" fill="#00ff00" class="live-indicator"/>
  <text x="228" y="162" font-family="'Arial', sans-serif" font-size="8" fill="#00ff00" font-weight="bold">LIVE</text>
  <text x="255" y="162" font-family="'Arial', sans-serif" font-size="8" fill="#484f58">• Updated at {update_time} BCN</text>
  <text x="440" y="162" font-family="'Arial', sans-serif" font-size="7" fill="#30363d">(~5min GitHub cache)</text>
</svg>'''
    
    # Add cache-control headers to prevent caching (GitHub will still cache ~5min)
    response = Response(svg, mimetype='image/svg+xml')
    
    # Generate ETag based on current minute to force refresh every minute
    etag_base = f"{datetime.utcnow().strftime('%Y%m%d%H%M')}"
    etag = hashlib.md5(etag_base.encode()).hexdigest()
    
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['ETag'] = f'"{etag}"'
    response.headers['Last-Modified'] = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:00 GMT')
    response.headers['Vary'] = 'Accept-Encoding'
    
    return response

@app.route('/health')
def health():
    return {'status': 'ok', 'service': 'github-widget'}

@app.route('/stats')
def get_stats():
    """Return request statistics"""
    now = datetime.utcnow()
    
    # Calculate requests in last hour
    one_hour_ago = datetime.utcnow().timestamp() - 3600
    recent_requests = [
        r for r in stats['requests_history'] 
        if r.timestamp() > one_hour_ago
    ]
    
    return {
        'total_requests': stats['total_requests'],
        'requests_last_hour': len(recent_requests),
        'last_request': stats['last_request'].isoformat() if stats['last_request'] else None,
        'estimated_cache_efficiency': f"{(1 - len(recent_requests) / max(stats['total_requests'], 1)) * 100:.1f}%"
    }

if __name__ == '__main__':
    # Use 0.0.0.0 for production (accessible from outside)
    # Use 127.0.0.1 for local development only
    app.run(host='0.0.0.0', port=5000, debug=False)
