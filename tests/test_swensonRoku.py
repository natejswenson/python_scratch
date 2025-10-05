"""Unit tests for swensonRoku module."""
import pytest
from unittest.mock import patch, Mock
from swensonRoku import roku_home, select_app, launch_app, get_apps


class TestRokuHome:
    """Tests for roku_home function."""

    @patch('swensonRoku.roku')
    def test_roku_home(self, mock_roku):
        """Test roku_home calls roku.home()."""
        roku_home()
        mock_roku.home.assert_called_once()


class TestSelectApp:
    """Tests for select_app function."""

    @patch('builtins.input', return_value='1')
    def test_select_first_app(self, mock_input):
        """Test selecting the first application."""
        apps = ['Netflix [12]', 'Hulu [34]', 'YouTube [56]']

        result = select_app(apps)

        assert result == '12'
        mock_input.assert_called_once()

    @patch('builtins.input', return_value='2')
    def test_select_middle_app(self, mock_input):
        """Test selecting a middle application."""
        apps = ['Netflix [12]', 'Hulu [34]', 'YouTube [56]']

        result = select_app(apps)

        assert result == '34'

    @patch('builtins.input', return_value='3')
    def test_select_last_app(self, mock_input):
        """Test selecting the last application."""
        apps = ['Netflix [12]', 'Hulu [34]', 'YouTube [56]']

        result = select_app(apps)

        assert result == '56'

    @patch('builtins.input', return_value='1')
    def test_select_app_single_item(self, mock_input):
        """Test selecting from a single application."""
        apps = ['Netflix [12]']

        result = select_app(apps)

        assert result == '12'

    @patch('builtins.input', return_value='2')
    def test_select_app_complex_id(self, mock_input):
        """Test selecting app with multi-digit ID."""
        apps = ['Netflix [1234]', 'Hulu [5678]']

        result = select_app(apps)

        assert result == '5678'


class TestLaunchApp:
    """Tests for launch_app function."""

    @patch('swensonRoku.roku')
    @patch('swensonRoku.select_app', return_value='12')
    def test_launch_app(self, mock_select_app, mock_roku):
        """Test launching an application."""
        mock_roku.apps = ['Netflix [12]', 'Hulu [34]']
        mock_app = Mock()
        mock_roku.__getitem__.return_value = mock_app

        launch_app()

        mock_select_app.assert_called_once_with(['Netflix [12]', 'Hulu [34]'])
        mock_roku.__getitem__.assert_called_once_with('12')
        mock_app.launch.assert_called_once()


class TestGetApps:
    """Tests for get_apps function."""

    @patch('swensonRoku.roku')
    @patch('builtins.print')
    def test_get_apps(self, mock_print, mock_roku):
        """Test getting and displaying all apps."""
        mock_roku.apps = ['Netflix [12]', 'Hulu [34]', 'YouTube [56]']

        get_apps()

        mock_print.assert_called_once_with(['Netflix [12]', 'Hulu [34]', 'YouTube [56]'])

    @patch('swensonRoku.roku')
    @patch('builtins.print')
    def test_get_apps_empty(self, mock_print, mock_roku):
        """Test getting apps when no apps are available."""
        mock_roku.apps = []

        get_apps()

        mock_print.assert_called_once_with([])
