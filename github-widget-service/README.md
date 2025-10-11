# GitHub Profile Widget Service

Dynamic SVG widget service for GitHub profile with live time and weather data.

## Features

- 🕐 Live Barcelona & New York time (minute precision)
- 🌤️ Real-time Barcelona weather from wttr.in
- ⚡ Animated pulsing "LIVE" indicator
- 📊 Built-in statistics endpoint
- 🎨 Beautiful gradients and SVG animations
- 🔄 Cache-optimized for GitHub (updates ~5 min)
- 🚀 Zero-commit deployment

## Important Note About Caching

GitHub caches all external images through their camo proxy for ~5 minutes, regardless of HTTP cache headers. This is a GitHub limitation, not a service issue. See [GITHUB_CACHE_SOLUTION.md](GITHUB_CACHE_SOLUTION.md) for detailed explanation.

## Quick Start

### Local Development

**With Poetry (Recommended):**
```bash
cd github-widget-service
poetry install
poetry run python app.py
```

**With pip:**
```bash
cd github-widget-service
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Visit: http://localhost:5000/widget.svg

### Run Tests

```bash
poetry run pytest tests/ -v --cov
```

## Deploy to Render.com

1. Push this directory to a GitHub repository
2. Go to [render.com](https://render.com) and create a new Web Service
3. Connect your GitHub repo
4. Select the `github-widget-service` folder as root directory
5. Render will auto-detect the `render.yaml` configuration
6. Deploy!

Your widget will be available at: `https://your-service.onrender.com/widget.svg`

## API Endpoints

### `GET /widget.svg`
Returns the live SVG widget with:
- Barcelona and New York current time
- Barcelona weather (temp, conditions, humidity, wind)
- Pulsing LIVE indicator
- Cache-busting support via query parameters

**Example:**
```bash
curl https://alexcolls.onrender.com/widget.svg
```

### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "service": "github-widget"
}
```

### `GET /stats`
Request statistics for monitoring.

**Response:**
```json
{
  "total_requests": 1234,
  "requests_last_hour": 42,
  "last_request": "2025-10-11T15:30:00.123456",
  "estimated_cache_efficiency": "95.5%"
}
```

## Usage in GitHub README

Once deployed, update your README.md:

```markdown
<a href="https://wttr.in/Barcelona">
  <img src="https://your-service.onrender.com/widget.svg?v=2025" alt="Barcelona Live Time & Weather" />
</a>
```

**Note:** The `?v=2025` query parameter is for cache-busting. Update it annually or when needed.

## Configuration

Copy `.env.sample` to `.env` and customize:

```bash
cp .env.sample .env
```

Key configuration options:
- `WEATHER_CITY` - City for weather data (default: Barcelona)
- `PRIMARY_TIMEZONE` - Main timezone (default: Europe/Madrid)
- `SECONDARY_TIMEZONE` - Second timezone (default: America/New_York)
- `FLASK_HOST` / `FLASK_PORT` - Server binding

See `.env.sample` for all available options.

## Development

### Project Structure
```
github-widget-service/
├── app.py                    # Main Flask application
├── tests/                    # Test suite
│   ├── __init__.py
│   └── test_widget.py       # Widget tests (19 tests, 99% coverage)
├── pyproject.toml           # Poetry configuration
├── requirements.txt         # Pip requirements (for Render)
├── render.yaml             # Render deployment config
├── .env.sample             # Environment variables template
├── .gitignore              # Git ignore rules
├── README.md               # This file
└── GITHUB_CACHE_SOLUTION.md # Caching explanation
```

### Adding Features

1. Make changes to `app.py`
2. Add tests in `tests/test_widget.py`
3. Run tests: `poetry run pytest -v`
4. Commit and push (Render auto-deploys)

## Technical Stack

- **Framework:** Flask 3.0.3
- **Server:** Gunicorn 22.0.0
- **Weather API:** wttr.in (free, no API key needed)
- **Python:** 3.11+
- **Deployment:** Render.com
- **Testing:** pytest with 99% coverage

## Troubleshooting

### Widget not updating on GitHub?
- This is expected - GitHub caches for ~5 minutes
- See [GITHUB_CACHE_SOLUTION.md](GITHUB_CACHE_SOLUTION.md) for details

### Weather showing "??"?
- wttr.in API might be temporarily down
- Service includes automatic fallback
- Check `/stats` endpoint to verify service is running

### Want faster updates?
- Not possible due to GitHub's camo proxy
- Options: Accept 5-min cache or use GitHub Actions (see docs)

## License

MIT License - see [LICENSE](../LICENSE) for details.

## Resources

- [GitHub Caching Explanation](GITHUB_CACHE_SOLUTION.md)
- [Render.com Documentation](https://render.com/docs)
- [wttr.in Weather API](https://github.com/chubin/wttr.in)
- [Flask Documentation](https://flask.palletsprojects.com/)
