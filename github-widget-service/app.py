from flask import Flask, Response
import requests
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route('/widget.svg')
def widget():
    """Generate time & weather widget SVG dynamically"""
    
    # Get Barcelona time
    bcn_tz = pytz.timezone('Europe/Madrid')
    now_bcn = datetime.now(bcn_tz)
    
    # Get New York time
    ny_tz = pytz.timezone('America/New_York')
    now_ny = datetime.now(ny_tz)
    
    # Format times
    bcn_time_str = now_bcn.strftime('%H:%M:%S')
    ny_time_str = now_ny.strftime('%H:%M:%S')
    date_str = now_bcn.strftime('%A, %B %d, %Y')
    
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
    
    # Create stunning SVG
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
  </defs>
  
  <!-- Background -->
  <rect width="600" height="170" rx="10" fill="url(#bgGrad)" stroke="#ff1493" stroke-width="3"/>
  
  <!-- Time Section -->
  <text x="20" y="28" font-family="'Courier New', monospace" font-size="12" fill="#00ff00" font-weight="bold">🏖️ BARCELONA</text>
  <text x="20" y="55" font-family="'Courier New', monospace" font-size="32" fill="url(#timeGrad)" font-weight="bold" filter="url(#glow)">{bcn_time_str}</text>
  <text x="20" y="70" font-family="'Arial', sans-serif" font-size="9" fill="#8b949e">{date_str}</text>
  
  <!-- New York Time -->
  <text x="20" y="100" font-family="'Courier New', monospace" font-size="12" fill="#58a6ff" font-weight="bold">🗽 NEW YORK</text>
  <text x="20" y="130" font-family="'Courier New', monospace" font-size="32" fill="#58a6ff" font-weight="bold">{ny_time_str}</text>
  
  <!-- Divider -->
  <line x1="300" y1="15" x2="300" y2="155" stroke="#30363d" stroke-width="2"/>
  
  <!-- Weather Section -->
  <text x="320" y="30" font-family="'Arial', sans-serif" font-size="14" fill="#00ff00" font-weight="bold">🌤️ BCN WEATHER</text>
  <text x="320" y="75" font-family="'Arial', sans-serif" font-size="40" fill="#ffffff" font-weight="bold">{icon} {temp}°C</text>
  <text x="320" y="100" font-family="'Arial', sans-serif" font-size="14" fill="#8b949e">{weather_desc}</text>
  <text x="320" y="125" font-family="'Arial', sans-serif" font-size="12" fill="#8b949e">Feels like {feels_like}°C • Humidity {humidity}%</text>
  <text x="320" y="145" font-family="'Arial', sans-serif" font-size="12" fill="#8b949e">Wind {wind_speed} km/h {wind_dir}</text>
  
  <!-- Footer -->
  <text x="300" y="162" font-family="'Arial', sans-serif" font-size="8" fill="#484f58" text-anchor="middle">Live • Updates on every visit</text>
</svg>'''
    
    # Add cache-control headers to prevent caching
    response = Response(svg, mimetype='image/svg+xml')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/health')
def health():
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
