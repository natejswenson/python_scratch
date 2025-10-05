"""Unit tests for github/create_repo module."""
import pytest
from unittest.mock import patch, Mock
from github.create_repo import create_github_repo


class TestCreateGithubRepo:
    """Tests for create_github_repo function."""

    @patch('github.create_repo.Github')
    def test_create_repo_success(self, mock_github_class):
        """Test successful repository creation."""
        # Mock Github instance
        mock_github = Mock()
        mock_github_class.return_value = mock_github

        # Mock user
        mock_user = Mock()
        mock_github.get_user.return_value = mock_user

        # Mock repository
        mock_repo = Mock()
        mock_repo.html_url = 'https://github.com/testuser/test-repo'
        mock_user.create_repo.return_value = mock_repo

        repo, error = create_github_repo(
            'test-repo',
            'A test repository',
            False,
            'test-token'
        )

        assert repo is not None
        assert error is None
        assert repo.html_url == 'https://github.com/testuser/test-repo'
        mock_user.create_repo.assert_called_once_with(
            'test-repo',
            description='A test repository',
            private=False
        )

    @patch('github.create_repo.Github')
    def test_create_private_repo(self, mock_github_class):
        """Test creating a private repository."""
        mock_github = Mock()
        mock_github_class.return_value = mock_github

        mock_user = Mock()
        mock_github.get_user.return_value = mock_user

        mock_repo = Mock()
        mock_repo.html_url = 'https://github.com/testuser/private-repo'
        mock_user.create_repo.return_value = mock_repo

        repo, error = create_github_repo(
            'private-repo',
            'A private repository',
            True,
            'test-token'
        )

        assert repo is not None
        assert error is None
        mock_user.create_repo.assert_called_once_with(
            'private-repo',
            description='A private repository',
            private=True
        )

    @patch('github.create_repo.Github')
    def test_create_repo_authentication_error(self, mock_github_class):
        """Test repository creation with authentication error."""
        mock_github = Mock()
        mock_github_class.return_value = mock_github

        mock_user = Mock()
        mock_github.get_user.return_value = mock_user
        mock_user.create_repo.side_effect = Exception("Bad credentials")

        repo, error = create_github_repo(
            'test-repo',
            'A test repository',
            False,
            'invalid-token'
        )

        assert repo is None
        assert error is not None
        assert "Bad credentials" in error

    @patch('github.create_repo.Github')
    def test_create_repo_already_exists(self, mock_github_class):
        """Test repository creation when repo already exists."""
        mock_github = Mock()
        mock_github_class.return_value = mock_github

        mock_user = Mock()
        mock_github.get_user.return_value = mock_user
        mock_user.create_repo.side_effect = Exception("Repository already exists")

        repo, error = create_github_repo(
            'existing-repo',
            'Already exists',
            False,
            'test-token'
        )

        assert repo is None
        assert error is not None
        assert "already exists" in error.lower()

    @patch('github.create_repo.Github')
    def test_create_repo_with_empty_description(self, mock_github_class):
        """Test creating repository with empty description."""
        mock_github = Mock()
        mock_github_class.return_value = mock_github

        mock_user = Mock()
        mock_github.get_user.return_value = mock_user

        mock_repo = Mock()
        mock_repo.html_url = 'https://github.com/testuser/no-desc-repo'
        mock_user.create_repo.return_value = mock_repo

        repo, error = create_github_repo(
            'no-desc-repo',
            '',
            False,
            'test-token'
        )

        assert repo is not None
        assert error is None
        mock_user.create_repo.assert_called_once_with(
            'no-desc-repo',
            description='',
            private=False
        )

    @patch('github.create_repo.Github')
    def test_create_repo_network_error(self, mock_github_class):
        """Test repository creation with network error."""
        mock_github_class.side_effect = Exception("Network error")

        repo, error = create_github_repo(
            'test-repo',
            'A test repository',
            False,
            'test-token'
        )

        assert repo is None
        assert error is not None
        assert "Network error" in error
