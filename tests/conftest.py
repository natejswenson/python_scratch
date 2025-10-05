"""Pytest configuration and fixtures."""
import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_response():
    """Create a mock HTTP response."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {}
    return response


@pytest.fixture
def mock_api_headers():
    """Create mock API headers."""
    return {
        'Authorization': 'Bearer test-token',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


@pytest.fixture
def sample_github_repo_data():
    """Sample GitHub repository data."""
    return {
        'name': 'test-repo',
        'description': 'A test repository',
        'stargazers_count': 100,
        'forks_count': 50,
        'private': False,
        'html_url': 'https://github.com/testuser/test-repo'
    }


@pytest.fixture
def sample_weather_data():
    """Sample weather API response data."""
    return {
        'location': {
            'name': 'New York',
            'region': 'New York',
            'country': 'USA'
        },
        'current': {
            'temperature': 72,
            'weather_descriptions': ['Partly cloudy'],
            'humidity': 65,
            'wind_speed': 10
        }
    }


@pytest.fixture
def sample_ip_data():
    """Sample IP geolocation data."""
    return {
        'ip': '192.168.1.1',
        'city': 'New York',
        'region': 'NY',
        'country': 'US',
        'zip': '10001',
        'status': 'success'
    }


@pytest.fixture
def sample_smartthings_devices():
    """Sample SmartThings device list."""
    device1 = Mock()
    device1.name = 'Living Room Light'
    device1.device_id = 'device-123'
    device1.capabilities = ['switch', 'level']

    device2 = Mock()
    device2.name = 'Bedroom Thermostat'
    device2.device_id = 'device-456'
    device2.capabilities = ['temperature', 'thermostat']

    return [device1, device2]


@pytest.fixture
def sample_roku_apps():
    """Sample Roku application list."""
    return [
        'Netflix [12]',
        'Hulu [34]',
        'YouTube [56]',
        'Amazon Prime [78]'
    ]


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response."""
    response = Mock()
    choice = Mock()
    message = Mock()
    message.content = 'This is a test response from OpenAI'
    choice.message = message
    response.choices = [choice]
    return response


# Auto-use fixtures for common test setup
@pytest.fixture(autouse=True)
def reset_environment(monkeypatch):
    """Reset environment variables for each test."""
    # This prevents tests from using real environment variables
    monkeypatch.delenv('github_pat', raising=False)
    monkeypatch.delenv('weather_pat', raising=False)
    monkeypatch.delenv('open_ai_pat', raising=False)
    monkeypatch.delenv('smart_things_pat', raising=False)
