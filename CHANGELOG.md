# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-10-11

### Added
- Dynamic GitHub profile widget service deployed on Render.com
- Live Barcelona and New York time display with timezone support
- Real-time Barcelona weather data from wttr.in API
- Pulsing "LIVE" indicator with CSS animations in SVG
- ETag-based cache control with minute-level precision
- `/stats` endpoint for monitoring widget request patterns
- Cache-busting query parameter support (`?v=2025`)
- Comprehensive test suite with pytest
- Poetry configuration for dependency management
- Environment variable configuration via `.env` files
- MIT License
- Comprehensive documentation explaining GitHub caching behavior
- Carousel GIF generator script for header images
- GitHub stats integration in README (light/dark mode)

### Changed
- Time display format from `HH:MM:SS` to `HH:MM` (optimized for 5-min cache)
- Increased font sizes for better visibility (time: 32→36, weather: 40→42)
- Updated README with honest caching expectations (~5 min updates)
- Improved widget footer with update timestamp and cache notice

### Fixed
- Host binding configuration for production deployment
- Cache control headers for non-GitHub viewers
- Graceful fallback when weather API is unavailable

### Technical
- Flask 3.0.3
- Python 3.11+
- Gunicorn WSGI server
- Render.com deployment
- wttr.in weather API integration

[unreleased]: https://github.com/alexcolls/alexcolls/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/alexcolls/alexcolls/releases/tag/v0.1.0
