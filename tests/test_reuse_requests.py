"""Unit tests for utils/reuse_requests module."""
import pytest
from unittest.mock import patch, Mock
from utils.reuse_requests import RequestsApi


class TestRequestsApi:
    """Tests for RequestsApi class."""

    def test_init_with_base_url(self):
        """Test initialization with base URL."""
        api = RequestsApi('https://api.example.com')
        assert api.base_url == 'https://api.example.com'

    def test_init_with_headers(self):
        """Test initialization with custom headers."""
        headers = {'Authorization': 'Bearer token123'}
        api = RequestsApi('https://api.example.com', headers=headers)
        assert api.session.headers['Authorization'] == 'Bearer token123'

    def test_init_with_multiple_kwargs(self):
        """Test initialization with multiple kwargs."""
        headers = {'User-Agent': 'TestBot/1.0'}
        api = RequestsApi(
            'https://api.example.com',
            headers=headers,
            timeout=30
        )
        assert api.session.headers['User-Agent'] == 'TestBot/1.0'
        assert api.session.timeout == 30

    @patch('utils.reuse_requests.requests.Session.get')
    def test_get_request(self, mock_get):
        """Test GET request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        api = RequestsApi('https://api.example.com')
        response = api.get('/users')

        assert response.status_code == 200
        mock_get.assert_called_once_with('https://api.example.com/users')

    @patch('utils.reuse_requests.requests.Session.post')
    def test_post_request(self, mock_post):
        """Test POST request."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        api = RequestsApi('https://api.example.com')
        response = api.post('/users', json={'name': 'John'})

        assert response.status_code == 201
        mock_post.assert_called_once_with(
            'https://api.example.com/users',
            json={'name': 'John'}
        )

    @patch('utils.reuse_requests.requests.Session.put')
    def test_put_request(self, mock_put):
        """Test PUT request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_put.return_value = mock_response

        api = RequestsApi('https://api.example.com')
        response = api.put('/users/1', json={'name': 'Jane'})

        assert response.status_code == 200
        mock_put.assert_called_once_with(
            'https://api.example.com/users/1',
            json={'name': 'Jane'}
        )

    @patch('utils.reuse_requests.requests.Session.patch')
    def test_patch_request(self, mock_patch):
        """Test PATCH request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_patch.return_value = mock_response

        api = RequestsApi('https://api.example.com')
        response = api.patch('/users/1', json={'status': 'active'})

        assert response.status_code == 200
        mock_patch.assert_called_once_with(
            'https://api.example.com/users/1',
            json={'status': 'active'}
        )

    @patch('utils.reuse_requests.requests.Session.delete')
    def test_delete_request(self, mock_delete):
        """Test DELETE request."""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_delete.return_value = mock_response

        api = RequestsApi('https://api.example.com')
        response = api.delete('/users/1')

        assert response.status_code == 204
        mock_delete.assert_called_once_with('https://api.example.com/users/1')

    @patch('utils.reuse_requests.requests.Session.head')
    def test_head_request(self, mock_head):
        """Test HEAD request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_head.return_value = mock_response

        api = RequestsApi('https://api.example.com')
        response = api.head('/users')

        assert response.status_code == 200
        mock_head.assert_called_once_with('https://api.example.com/users')

    @patch('utils.reuse_requests.requests.Session.request')
    def test_custom_request_method(self, mock_request):
        """Test custom request method."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        api = RequestsApi('https://api.example.com')
        response = api.request('OPTIONS', '/users')

        assert response.status_code == 200
        mock_request.assert_called_once_with('OPTIONS', 'https://api.example.com/users')

    @patch('utils.reuse_requests.requests.Session.get')
    def test_get_with_params(self, mock_get):
        """Test GET request with query parameters."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        api = RequestsApi('https://api.example.com')
        response = api.get('/users', params={'page': 1, 'limit': 10})

        mock_get.assert_called_once_with(
            'https://api.example.com/users',
            params={'page': 1, 'limit': 10}
        )

    def test_deep_merge_headers(self):
        """Test deep merge of headers."""
        api = RequestsApi(
            'https://api.example.com',
            headers={'Authorization': 'Bearer token', 'Accept': 'application/json'}
        )
        assert api.session.headers['Authorization'] == 'Bearer token'
        assert api.session.headers['Accept'] == 'application/json'

    @patch('utils.reuse_requests.requests.Session.get')
    def test_base_url_concatenation(self, mock_get):
        """Test that base URL and path are properly concatenated."""
        mock_response = Mock()
        mock_get.return_value = mock_response

        api = RequestsApi('https://api.example.com/v1')
        api.get('/users/123')

        mock_get.assert_called_once_with('https://api.example.com/v1/users/123')
