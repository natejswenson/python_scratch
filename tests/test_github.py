"""Unit tests for github module."""
import pytest
from unittest.mock import patch, Mock, mock_open
from github import get_repo_info


class TestGetRepoInfo:
    """Tests for get_repo_info function."""

    @patch('github.reuse_requests.get')
    def test_get_repo_info_success(self, mock_get):
        """Test successful repository information retrieval."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'name': 'test-repo',
            'description': 'A test repository',
            'stargazers_count': 100,
            'forks_count': 50
        }
        mock_get.return_value = mock_response

        headers = {'Authorization': 'Token test_token'}
        result = get_repo_info('testuser', 'test-repo', headers)

        assert result is not None
        assert result['name'] == 'test-repo'
        assert result['stargazers_count'] == 100
        mock_get.assert_called_once_with(
            'https://api.github.com/repos/testuser/test-repo',
            headers=headers
        )

    @patch('github.reuse_requests.get')
    def test_get_repo_info_not_found(self, mock_get):
        """Test repository not found (404)."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        headers = {'Authorization': 'Token test_token'}
        result = get_repo_info('testuser', 'nonexistent-repo', headers)

        assert result is None

    @patch('github.reuse_requests.get')
    def test_get_repo_info_unauthorized(self, mock_get):
        """Test unauthorized access (401)."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        headers = {'Authorization': 'Token invalid_token'}
        result = get_repo_info('testuser', 'test-repo', headers)

        assert result is None

    @patch('github.reuse_requests.get')
    def test_get_repo_info_exception(self, mock_get):
        """Test exception handling."""
        mock_get.side_effect = Exception("Network error")

        headers = {'Authorization': 'Token test_token'}
        result = get_repo_info('testuser', 'test-repo', headers)

        assert result is None

    @patch('github.reuse_requests.get')
    def test_get_repo_info_rate_limited(self, mock_get):
        """Test rate limiting (403)."""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_get.return_value = mock_response

        headers = {'Authorization': 'Token test_token'}
        result = get_repo_info('testuser', 'test-repo', headers)

        assert result is None

    @patch('github.reuse_requests.get')
    def test_get_repo_info_private_repo(self, mock_get):
        """Test accessing private repository."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'name': 'private-repo',
            'description': 'A private repository',
            'stargazers_count': 10,
            'forks_count': 2,
            'private': True
        }
        mock_get.return_value = mock_response

        headers = {'Authorization': 'Token test_token'}
        result = get_repo_info('testuser', 'private-repo', headers)

        assert result is not None
        assert result['private'] is True
