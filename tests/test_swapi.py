"""Unit tests for SWAPI function - TDD approach."""
import pytest
from unittest.mock import patch, Mock
from requests.exceptions import HTTPError, Timeout, RequestException
from swapi import get_swapi_data, SWAPIResource, SWAPIError


class TestInputValidation:
    """Test input parameter validation."""

    def test_valid_resource_type_accepted(self):
        """Test that valid resource types are accepted."""
        with patch('swapi.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {"name": "Luke Skywalker"}

            result = get_swapi_data(SWAPIResource.PEOPLE, resource_id=1)
            assert result is not None

    def test_invalid_resource_type_raises_error(self):
        """Test that invalid resource type raises ValueError."""
        with pytest.raises((ValueError, AttributeError)):
            get_swapi_data("invalid_type", resource_id=1)

    def test_negative_resource_id_raises_error(self):
        """Test that negative resource ID raises ValueError."""
        with pytest.raises(ValueError, match="resource_id must be positive"):
            get_swapi_data(SWAPIResource.PEOPLE, resource_id=-1)

    def test_zero_resource_id_raises_error(self):
        """Test that zero resource ID raises ValueError."""
        with pytest.raises(ValueError, match="resource_id must be positive"):
            get_swapi_data(SWAPIResource.PEOPLE, resource_id=0)

    def test_invalid_page_number_raises_error(self):
        """Test that invalid page number raises ValueError."""
        with pytest.raises(ValueError, match="page must be positive"):
            get_swapi_data(SWAPIResource.PEOPLE, page=-1)

    def test_conflicting_params_raises_error(self):
        """Test that resource_id and search together raise ValueError."""
        with pytest.raises(ValueError, match="Cannot specify both"):
            get_swapi_data(SWAPIResource.PEOPLE, resource_id=1, search="Luke")


class TestURLConstruction:
    """Test URL construction logic."""

    @patch('swapi.requests.get')
    def test_url_for_resource_id(self, mock_get):
        """Test URL construction for resource ID."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"name": "Luke"}

        get_swapi_data(SWAPIResource.PEOPLE, resource_id=1)

        mock_get.assert_called_once()
        assert "people/1" in mock_get.call_args[0][0]

    @patch('swapi.requests.get')
    def test_url_for_search(self, mock_get):
        """Test URL construction for search."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "count": 1,
            "results": [{"name": "Luke"}]
        }

        get_swapi_data(SWAPIResource.PEOPLE, search="Luke")

        mock_get.assert_called_once()
        call_url = mock_get.call_args[0][0]
        assert "people/" in call_url
        assert "search=Luke" in call_url

    @patch('swapi.requests.get')
    def test_url_for_pagination(self, mock_get):
        """Test URL construction for specific page."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "count": 10,
            "results": []
        }

        get_swapi_data(SWAPIResource.PEOPLE, page=2)

        mock_get.assert_called_once()
        assert "page=2" in mock_get.call_args[0][0]

    @patch('swapi.requests.get')
    def test_base_url_correct(self, mock_get):
        """Test that base URL is correct."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"name": "Tatooine"}

        get_swapi_data(SWAPIResource.PLANETS, resource_id=1)

        assert mock_get.call_args[0][0].startswith("https://swapi.dev/api/")


class TestResponseParsing:
    """Test response parsing logic."""

    @patch('swapi.requests.get')
    def test_parse_single_resource(self, mock_get):
        """Test parsing single resource response."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "name": "Luke Skywalker",
            "height": "172"
        }

        result = get_swapi_data(SWAPIResource.PEOPLE, resource_id=1)

        assert isinstance(result, dict)
        assert result["name"] == "Luke Skywalker"

    @patch('swapi.requests.get')
    def test_parse_list_of_resources(self, mock_get):
        """Test parsing list of resources."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "count": 2,
            "results": [
                {"name": "Luke"},
                {"name": "Leia"}
            ]
        }

        result = get_swapi_data(SWAPIResource.PEOPLE, search="L")

        assert isinstance(result, list)
        assert len(result) == 2

    @patch('swapi.requests.get')
    def test_parse_empty_results(self, mock_get):
        """Test parsing empty search results."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "count": 0,
            "results": []
        }

        result = get_swapi_data(SWAPIResource.PEOPLE, search="Nonexistent")

        assert isinstance(result, list)
        assert len(result) == 0

    @patch('swapi.requests.get')
    def test_parse_malformed_json_raises_error(self, mock_get):
        """Test that malformed JSON raises error."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.side_effect = ValueError("Invalid JSON")

        with pytest.raises(SWAPIError, match="Failed to parse"):
            get_swapi_data(SWAPIResource.PEOPLE, resource_id=1)


class TestErrorHandling:
    """Test error handling."""

    @patch('swapi.requests.get')
    def test_404_not_found(self, mock_get):
        """Test 404 error handling."""
        mock_get.return_value.status_code = 404
        mock_get.return_value.raise_for_status.side_effect = HTTPError("Not found")

        with pytest.raises(SWAPIError, match="Resource not found"):
            get_swapi_data(SWAPIResource.PEOPLE, resource_id=9999)

    @patch('swapi.requests.get')
    def test_500_server_error(self, mock_get):
        """Test 500 server error handling."""
        mock_get.return_value.status_code = 500
        mock_get.return_value.raise_for_status.side_effect = HTTPError("Server error")

        with pytest.raises(SWAPIError, match="Server error"):
            get_swapi_data(SWAPIResource.PEOPLE, resource_id=1)

    @patch('swapi.requests.get')
    def test_timeout_error(self, mock_get):
        """Test timeout error handling."""
        mock_get.side_effect = Timeout("Request timeout")

        with pytest.raises(SWAPIError, match="Request timeout"):
            get_swapi_data(SWAPIResource.PEOPLE, resource_id=1)

    @patch('swapi.requests.get')
    def test_connection_error(self, mock_get):
        """Test connection error handling."""
        mock_get.side_effect = RequestException("Connection failed")

        with pytest.raises(SWAPIError, match="Network error"):
            get_swapi_data(SWAPIResource.PEOPLE, resource_id=1)


class TestCaching:
    """Test caching functionality."""

    @patch('swapi.requests.get')
    def test_cache_stores_result(self, mock_get):
        """Test that results are cached."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"name": "Luke"}

        # First call
        result1 = get_swapi_data(SWAPIResource.PEOPLE, resource_id=1, use_cache=True)
        # Second call should use cache
        result2 = get_swapi_data(SWAPIResource.PEOPLE, resource_id=1, use_cache=True)

        # Should only make one API call
        assert mock_get.call_count == 1
        assert result1 == result2

    @patch('swapi.requests.get')
    def test_cache_disabled_makes_request(self, mock_get):
        """Test that cache can be disabled."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"name": "Luke"}

        get_swapi_data(SWAPIResource.PEOPLE, resource_id=1, use_cache=False)
        get_swapi_data(SWAPIResource.PEOPLE, resource_id=1, use_cache=False)

        # Should make two API calls
        assert mock_get.call_count == 2


class TestSearchFunctionality:
    """Test search functionality."""

    @patch('swapi.requests.get')
    def test_search_exact_match(self, mock_get):
        """Test search with exact match."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "count": 1,
            "results": [{"name": "Luke Skywalker"}]
        }

        result = get_swapi_data(SWAPIResource.PEOPLE, search="Luke Skywalker")

        assert len(result) == 1
        assert result[0]["name"] == "Luke Skywalker"

    @patch('swapi.requests.get')
    def test_search_partial_match(self, mock_get):
        """Test search with partial match."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "count": 2,
            "results": [
                {"name": "Luke Skywalker"},
                {"name": "Leia Organa"}
            ]
        }

        result = get_swapi_data(SWAPIResource.PEOPLE, search="L")

        assert len(result) == 2

    @patch('swapi.requests.get')
    def test_search_no_results(self, mock_get):
        """Test search with no results."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "count": 0,
            "results": []
        }

        result = get_swapi_data(SWAPIResource.PEOPLE, search="XYZ123")

        assert result == []


class TestPagination:
    """Test pagination functionality."""

    @patch('swapi.requests.get')
    def test_get_specific_page(self, mock_get):
        """Test getting a specific page."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "count": 20,
            "next": None,
            "previous": "https://swapi.dev/api/people/?page=1",
            "results": [{"name": "Person on page 2"}]
        }

        result = get_swapi_data(SWAPIResource.PEOPLE, page=2)

        assert "page=2" in mock_get.call_args[0][0]

    @patch('swapi.requests.get')
    def test_single_page_no_pagination(self, mock_get):
        """Test single page with no pagination needed."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "count": 5,
            "next": None,
            "previous": None,
            "results": [{"name": f"Item {i}"} for i in range(5)]
        }

        result = get_swapi_data(SWAPIResource.FILMS)

        assert len(result) == 5
        assert mock_get.call_count == 1


class TestURLResolution:
    """Test URL resolution functionality."""

    @patch('swapi.requests.get')
    def test_resolve_disabled_returns_urls(self, mock_get):
        """Test that URLs are returned when resolution is disabled."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "name": "Luke",
            "homeworld": "https://swapi.dev/api/planets/1/"
        }

        result = get_swapi_data(
            SWAPIResource.PEOPLE,
            resource_id=1,
            resolve_urls=False
        )

        assert result["homeworld"] == "https://swapi.dev/api/planets/1/"
        assert mock_get.call_count == 1


class TestTimeoutConfiguration:
    """Test timeout configuration."""

    @patch('swapi.requests.get')
    def test_custom_timeout_used(self, mock_get):
        """Test that custom timeout is used."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"name": "Luke"}

        get_swapi_data(SWAPIResource.PEOPLE, resource_id=1, timeout=5)

        assert mock_get.call_args[1]['timeout'] == 5

    @patch('swapi.requests.get')
    def test_default_timeout_used(self, mock_get):
        """Test that default timeout is used."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"name": "Luke"}

        get_swapi_data(SWAPIResource.PEOPLE, resource_id=1)

        assert mock_get.call_args[1]['timeout'] == 10
