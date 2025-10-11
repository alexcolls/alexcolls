# GitHub Profile Widget - Cache Solution

## The Problem

GitHub aggressively caches all external images displayed in README files through their [camo proxy](https://github.blog/2010-11-13-sidejack-prevention-phase-3-ssl-proxied-assets/). This means:

- **Cache Duration**: ~5 minutes minimum, regardless of HTTP cache headers
- **Ignores Headers**: GitHub's camo proxy ignores `Cache-Control`, `Pragma`, and `Expires` headers
- **No Bypass**: There's no official way to force real-time updates without commits

## What We Tried

1. ✅ **Render.com Dynamic Service** - Works perfectly, generates SVG on every request
2. ❌ **HTTP Cache Headers** - GitHub's camo ignores them completely
3. ❌ **True Real-Time Updates** - Impossible due to GitHub's proxy architecture

## The Solution (What We Implemented)

Since we can't fight GitHub's cache, we **optimized for the reality** of ~5 minute updates:

### 1. **Removed Unnecessary Precision** 
- Changed time display from `HH:MM:SS` to `HH:MM`
- No point showing seconds when the widget updates every 5 minutes

### 2. **Added Transparency**
- Pulsing "LIVE" indicator (with CSS animation)
- "Updated at HH:MM BCN" timestamp
- Footer note: "(~5min GitHub cache)"
- This sets proper expectations for visitors

### 3. **Improved Cache Headers (For Non-GitHub Viewers)**
```python
ETag: MD5 hash based on current minute
Last-Modified: Current time rounded to minute
Cache-Control: no-cache, no-store, must-revalidate, max-age=0
Vary: Accept-Encoding
```

### 4. **Cache-Busting Query Parameter**
- URL: `https://alexcolls.onrender.com/widget.svg?v=2025`
- The `?v=2025` parameter can be updated annually to force refresh if needed
- Doesn't affect the service (query params are ignored)

### 5. **Monitoring Endpoint**
```bash
curl https://alexcolls.onrender.com/stats
```
Returns:
- Total requests
- Requests in last hour
- Last request timestamp
- Estimated cache efficiency

### 6. **Visual Improvements**
- Increased font sizes (32→36 for time, 40→42 for weather)
- More prominent weather display
- Better spacing and alignment

## Current Behavior

✅ **What Works:**
- Widget generates fresh data on server side every request
- Barcelona & NYC times are accurate (to the minute)
- Live weather data from wttr.in
- Beautiful pulsing LIVE indicator
- Proper cache headers for non-GitHub viewers

⏰ **What's Limited by GitHub:**
- Widget updates ~every 5 minutes due to camo proxy
- Different users may see slightly different cached versions
- No way to force immediate refresh without pushing commits

## Alternative Solutions (Not Implemented)

### Option A: GitHub Actions (What Most People Do)
```yaml
# .github/workflows/update-widget.yml
schedule:
  - cron: '*/5 * * * *'  # Every 5 minutes
```
- Updates widget via commits
- Pollutes git history with automated commits
- Requires GitHub Actions quota
- **We avoided this to keep repo clean**

### Option B: Accept Static Widget
- Generate once daily/weekly
- Commit as static SVG
- Much simpler but not "live"

### Option C: Use GitHub's API Directly
- Create custom GitHub Action badge
- Limited styling options
- Still subject to caching

## Why This Approach is Better

1. **Clean Git History** - No automated commits
2. **True Server-Side Generation** - Weather data is always fresh on server
3. **Honest UX** - We acknowledge the cache instead of pretending it's real-time
4. **Best Possible Under Constraints** - ~5 min updates is the GitHub limit
5. **Monitoring Built-In** - Can track actual request patterns

## Testing the Widget

### Local Testing:
```bash
cd github-widget-service
python3 -m venv .venv
source .venv/bin/activate  # or `.venv/bin/activate` on Linux
pip install -r requirements.txt
python app.py

# In another terminal:
curl http://localhost:5000/widget.svg
curl http://localhost:5000/stats
```

### Production Testing:
```bash
# Check headers
curl -I https://alexcolls.onrender.com/widget.svg

# Get stats
curl https://alexcolls.onrender.com/stats

# View widget (saves to file)
curl https://alexcolls.onrender.com/widget.svg -o widget.svg
```

## Deployment to Render.com

The service auto-deploys via `render.yaml`:

```yaml
services:
  - type: web
    name: github-widget-service
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
```

### To Update in Production:
1. Push changes to GitHub
2. Render auto-detects and deploys
3. Widget URL remains the same
4. GitHub's cache expires in ~5 min

## The Truth About "Real-Time" GitHub Widgets

**Reality Check**: Any GitHub README widget claiming "real-time" or "live" updates is either:
1. Lying (subject to same caching)
2. Using GitHub Actions to commit every N minutes (polluting git history)
3. Showing static/old data

**Our approach**: Be honest about the limitations and make the best widget possible within those constraints.

## Next Steps (Optional Improvements)

1. **Add Poetry Configuration** (following user preferences)
2. **Create `.env.sample`** for configuration
3. **Add proper tests** (pytest)
4. **Rate Limiting** to prevent abuse
5. **Caching Weather Data** (weather doesn't change every minute)
6. **Fallback Images** if service is down
7. **More Timezones** (Tokyo, London, etc.)

## Resources

- [GitHub Camo Proxy Documentation](https://github.blog/2010-11-13-sidejack-prevention-phase-3-ssl-proxied-assets/)
- [Render.com Docs](https://render.com/docs)
- [wttr.in Weather API](https://github.com/chubin/wttr.in)
- [SVG Animations in Markdown](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/animate)

---

**TL;DR**: GitHub caches everything for ~5 minutes. We optimized the widget for this reality instead of fighting it. The result is honest, beautiful, and as "live" as GitHub allows. 🎯
