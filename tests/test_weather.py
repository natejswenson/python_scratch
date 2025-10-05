"""Unit tests for weather module."""
import pytest
from unittest.mock import patch, Mock
import requests
from weather import get_temp_based_on_ip, get_zipcode, get_public_ip


class TestGetPublicIP:
    """Tests for get_public_ip function."""

    @patch('weather.requests.get')
    def test_get_public_ip_success(self, mock_get):
        """Test successful IP retrieval."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'ip': '192.168.1.1'}
        mock_get.return_value = mock_response

        result = get_public_ip()
        assert result == '192.168.1.1'
        mock_get.assert_called_once()

    @patch('weather.requests.get')
    def test_get_public_ip_no_ip_in_response(self, mock_get):
        """Test when response doesn't contain IP."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        result = get_public_ip()
        assert result is None

    @patch('weather.requests.get')
    def test_get_public_ip_failed_request(self, mock_get):
        """Test failed HTTP request."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = get_public_ip()
        assert result is None

    @patch('weather.requests.get')
    def test_get_public_ip_network_error(self, mock_get):
        """Test network error handling."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

        result = get_public_ip()
        assert result is None

    @patch('weather.requests.get')
    def test_get_public_ip_json_error(self, mock_get):
        """Test JSON parsing error."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response

        result = get_public_ip()
        assert result is None


class TestGetZipcode:
    """Tests for get_zipcode function."""

    @patch('weather.get_public_ip')
    @patch('weather.requests.get')
    def test_get_zipcode_success(self, mock_get, mock_public_ip):
        """Test successful zipcode retrieval."""
        mock_public_ip.return_value = '192.168.1.1'
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'zip': '12345', 'status': 'success'}
        mock_get.return_value = mock_response

        result = get_zipcode()
        assert result == '12345'

    @patch('weather.get_public_ip')
    def test_get_zipcode_no_public_ip(self, mock_public_ip):
        """Test when public IP cannot be retrieved."""
        mock_public_ip.return_value = None

        result = get_zipcode()
        assert result is None

    @patch('weather.get_public_ip')
    @patch('weather.requests.get')
    def test_get_zipcode_api_fail_status(self, mock_get, mock_public_ip):
        """Test when API returns fail status."""
        mock_public_ip.return_value = '192.168.1.1'
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'status': 'fail', 'message': 'Invalid IP'}
        mock_get.return_value = mock_response

        result = get_zipcode()
        assert result is None

    @patch('weather.get_public_ip')
    @patch('weather.requests.get')
    def test_get_zipcode_no_zip_in_response(self, mock_get, mock_public_ip):
        """Test when response doesn't contain zip code."""
        mock_public_ip.return_value = '192.168.1.1'
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'status': 'success'}
        mock_get.return_value = mock_response

        result = get_zipcode()
        assert result is None

    @patch('weather.get_public_ip')
    @patch('weather.requests.get')
    def test_get_zipcode_network_error(self, mock_get, mock_public_ip):
        """Test network error handling."""
        mock_public_ip.return_value = '192.168.1.1'
        mock_get.side_effect = requests.exceptions.Timeout("Timeout")

        result = get_zipcode()
        assert result is None


class TestGetTempBasedOnIP:
    """Tests for get_temp_based_on_ip function."""

    @patch('weather.requests.get')
    def test_get_temp_success(self, mock_get):
        """Test successful temperature retrieval."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'location': {'name': 'New York'},
            'current': {'temperature': 72}
        }
        mock_get.return_value = mock_response

        result = get_temp_based_on_ip('10001')
        assert result is not None
        assert result['current']['temperature'] == 72

    @patch('weather.requests.get')
    def test_get_temp_api_error(self, mock_get):
        """Test when API returns error."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'error': {'info': 'Invalid API key'}
        }
        mock_get.return_value = mock_response

        result = get_temp_based_on_ip('10001')
        assert result is None

    @patch('weather.requests.get')
    def test_get_temp_http_error(self, mock_get):
        """Test HTTP error handling."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = get_temp_based_on_ip('10001')
        assert result is None

    @patch('weather.requests.get')
    def test_get_temp_network_error(self, mock_get):
        """Test network error handling."""
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        result = get_temp_based_on_ip('10001')
        assert result is None

    @patch('weather.requests.get')
    def test_get_temp_missing_data(self, mock_get):
        """Test when response is missing expected data."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'location': {}}
        mock_get.return_value = mock_response

        result = get_temp_based_on_ip('10001')
        assert result is None
