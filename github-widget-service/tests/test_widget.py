"""Tests for the widget service."""
import pytest
from datetime import datetime
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHealthEndpoint:
    """Tests for the /health endpoint."""

    def test_health_endpoint_returns_200(self, client):
        """Test that health endpoint returns 200 OK."""
        response = client.get('/health')
        assert response.status_code == 200

    def test_health_endpoint_returns_json(self, client):
        """Test that health endpoint returns JSON."""
        response = client.get('/health')
        assert response.content_type == 'application/json'

    def test_health_endpoint_structure(self, client):
        """Test that health endpoint returns expected structure."""
        response = client.get('/health')
        data = response.get_json()
        assert 'status' in data
        assert data['status'] == 'ok'
        assert 'service' in data
        assert data['service'] == 'github-widget'


class TestStatsEndpoint:
    """Tests for the /stats endpoint."""

    def test_stats_endpoint_returns_200(self, client):
        """Test that stats endpoint returns 200 OK."""
        response = client.get('/stats')
        assert response.status_code == 200

    def test_stats_endpoint_returns_json(self, client):
        """Test that stats endpoint returns JSON."""
        response = client.get('/stats')
        assert response.content_type == 'application/json'

    def test_stats_endpoint_structure(self, client):
        """Test that stats endpoint returns expected structure."""
        response = client.get('/stats')
        data = response.get_json()
        assert 'total_requests' in data
        assert 'requests_last_hour' in data
        assert 'estimated_cache_efficiency' in data
        assert isinstance(data['total_requests'], int)


class TestWidgetEndpoint:
    """Tests for the /widget.svg endpoint."""

    def test_widget_endpoint_returns_200(self, client):
        """Test that widget endpoint returns 200 OK."""
        response = client.get('/widget.svg')
        assert response.status_code == 200

    def test_widget_endpoint_returns_svg(self, client):
        """Test that widget endpoint returns SVG content type."""
        response = client.get('/widget.svg')
        assert response.content_type == 'image/svg+xml; charset=utf-8'

    def test_widget_endpoint_returns_svg_content(self, client):
        """Test that widget endpoint returns valid SVG content."""
        response = client.get('/widget.svg')
        data = response.data.decode('utf-8')
        assert data.startswith('<svg')
        assert data.endswith('</svg>')
        assert 'BARCELONA' in data
        assert 'NEW YORK' in data
        assert 'BCN WEATHER' in data

    def test_widget_has_cache_control_headers(self, client):
        """Test that widget has proper cache control headers."""
        response = client.get('/widget.svg')
        assert 'Cache-Control' in response.headers
        assert 'no-cache' in response.headers['Cache-Control']
        assert 'ETag' in response.headers
        assert 'Last-Modified' in response.headers
        assert 'Vary' in response.headers

    def test_widget_with_query_parameters(self, client):
        """Test that widget works with query parameters (cache busting)."""
        response1 = client.get('/widget.svg')
        response2 = client.get('/widget.svg?v=2025')
        response3 = client.get('/widget.svg?t=12345')
        
        # All should return 200
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        
        # Content should be similar (times might differ by seconds)
        assert 'BARCELONA' in response1.data.decode('utf-8')
        assert 'BARCELONA' in response2.data.decode('utf-8')
        assert 'BARCELONA' in response3.data.decode('utf-8')

    def test_widget_contains_time(self, client):
        """Test that widget contains time information."""
        response = client.get('/widget.svg')
        data = response.data.decode('utf-8')
        # Should contain HH:MM format times
        import re
        time_pattern = r'\d{2}:\d{2}'
        matches = re.findall(time_pattern, data)
        assert len(matches) >= 2  # At least Barcelona and NYC times

    def test_widget_contains_live_indicator(self, client):
        """Test that widget contains LIVE indicator."""
        response = client.get('/widget.svg')
        data = response.data.decode('utf-8')
        assert 'LIVE' in data
        assert 'live-indicator' in data
        assert 'pulse' in data  # CSS animation

    def test_widget_contains_cache_notice(self, client):
        """Test that widget contains GitHub cache notice."""
        response = client.get('/widget.svg')
        data = response.data.decode('utf-8')
        assert '5min GitHub cache' in data

    def test_widget_increments_stats(self, client):
        """Test that widget requests increment stats."""
        # Get initial stats
        stats_response = client.get('/stats')
        initial_stats = stats_response.get_json()
        initial_count = initial_stats['total_requests']
        
        # Make a widget request
        client.get('/widget.svg')
        
        # Check stats increased
        stats_response = client.get('/stats')
        new_stats = stats_response.get_json()
        assert new_stats['total_requests'] > initial_count


class TestWeatherFallback:
    """Tests for weather API fallback behavior."""

    def test_widget_handles_weather_api_failure_gracefully(self, client, monkeypatch):
        """Test that widget handles weather API failures gracefully."""
        # Mock requests.get to simulate API failure
        import requests
        
        def mock_get(*args, **kwargs):
            raise requests.exceptions.Timeout("API timeout")
        
        monkeypatch.setattr(requests, 'get', mock_get)
        
        response = client.get('/widget.svg')
        assert response.status_code == 200
        data = response.data.decode('utf-8')
        
        # Should contain fallback data
        assert '??' in data or 'Loading' in data


class TestSVGStructure:
    """Tests for SVG structure and elements."""

    def test_svg_has_proper_dimensions(self, client):
        """Test that SVG has expected dimensions."""
        response = client.get('/widget.svg')
        data = response.data.decode('utf-8')
        assert 'width="600"' in data
        assert 'height="170"' in data

    def test_svg_has_gradients(self, client):
        """Test that SVG contains gradient definitions."""
        response = client.get('/widget.svg')
        data = response.data.decode('utf-8')
        assert 'linearGradient' in data
        assert 'bgGrad' in data
        assert 'timeGrad' in data

    def test_svg_has_animations(self, client):
        """Test that SVG contains CSS animations."""
        response = client.get('/widget.svg')
        data = response.data.decode('utf-8')
        assert '@keyframes pulse' in data
        assert 'animation:' in data
