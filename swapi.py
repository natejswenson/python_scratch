"""
Star Wars API (SWAPI) integration module.

This module provides a simple, type-safe interface to the Star Wars API (SWAPI),
allowing retrieval of information about people, planets, starships, vehicles,
species, and films from the Star Wars universe.

Example:
    >>> from swapi import get_swapi_data, SWAPIResource
    >>> luke = get_swapi_data(SWAPIResource.PEOPLE, resource_id=1)
    >>> print(luke['name'])
    'Luke Skywalker'

    >>> planets = get_swapi_data(SWAPIResource.PLANETS, search="Tatooine")
    >>> print(planets[0]['climate'])
    'arid'
"""
from typing import Optional, Dict, List, Union, Any
from enum import Enum
import requests
import logging

# Configure logging
logger = logging.getLogger(__name__)


class SWAPIResource(Enum):
    """
    SWAPI resource types.

    Available resource types for querying the Star Wars API:
    - PEOPLE: Characters from Star Wars
    - PLANETS: Planets in the Star Wars universe
    - STARSHIPS: Starships and capital ships
    - VEHICLES: Ground and atmospheric vehicles
    - SPECIES: Species of creatures and characters
    - FILMS: Star Wars films
    """
    PEOPLE = "people"
    PLANETS = "planets"
    STARSHIPS = "starships"
    VEHICLES = "vehicles"
    SPECIES = "species"
    FILMS = "films"


class SWAPIError(Exception):
    """
    Custom exception for SWAPI-related errors.

    This exception is raised for:
    - Network errors (connection failures, timeouts)
    - HTTP errors (404, 500, etc.)
    - JSON parsing errors
    - API-specific errors
    """
    pass


# Simple in-memory cache
_cache: Dict[str, Union[Dict, List[Dict]]] = {}


def get_swapi_data(
    resource_type: SWAPIResource,
    resource_id: Optional[int] = None,
    search: Optional[str] = None,
    page: Optional[int] = None,
    resolve_urls: bool = False,
    use_cache: bool = True,
    timeout: int = 10
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Retrieve data from the Star Wars API (SWAPI).

    This function provides a unified interface to fetch Star Wars data with support
    for single resource retrieval, searching, and pagination. Results can be cached
    to minimize API calls.

    Args:
        resource_type: Type of SWAPI resource to retrieve (people, planets, etc.)
        resource_id: Specific resource ID to fetch. Must be positive integer.
        search: Search term for filtering results. Case-insensitive partial matching.
        page: Specific page number for paginated results. Must be positive integer.
        resolve_urls: If True, resolve related resource URLs to actual data (not implemented)
        use_cache: If True, use cached responses to reduce API calls
        timeout: Request timeout in seconds (default: 10)

    Returns:
        - Dict: When resource_id is specified, returns single resource data
        - List[Dict]: When searching or listing, returns list of resources

    Raises:
        ValueError: If invalid parameters are provided:
            - Negative or zero resource_id
            - Negative or zero page number
            - Both resource_id and search specified
        SWAPIError: For API-related errors:
            - Resource not found (404)
            - Server errors (500, 503, etc.)
            - Network errors (connection timeout, DNS failure)
            - JSON parsing errors

    Example:
        >>> # Get Luke Skywalker
        >>> luke = get_swapi_data(SWAPIResource.PEOPLE, resource_id=1)
        >>> print(f"{luke['name']} is {luke['height']}cm tall")
        Luke Skywalker is 172cm tall

        >>> # Search for planets
        >>> deserts = get_swapi_data(SWAPIResource.PLANETS, search="desert")
        >>> for planet in deserts:
        ...     print(planet['name'])

        >>> # Get all films (with caching)
        >>> films = get_swapi_data(SWAPIResource.FILMS, use_cache=True)
        >>> print(f"Found {len(films)} Star Wars films")
    """
    # Validate inputs
    _validate_inputs(resource_id, search, page)

    # Build cache key
    cache_key = _build_cache_key(resource_type, resource_id, search, page)

    # Check cache
    if use_cache and cache_key in _cache:
        return _cache[cache_key]

    # Build URL
    url = _build_url(resource_type, resource_id, search, page)

    # Make request
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise SWAPIError("Request timeout")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            raise SWAPIError("Resource not found")
        else:
            raise SWAPIError(f"Server error: {e}")
    except requests.exceptions.RequestException as e:
        raise SWAPIError(f"Network error: {e}")

    # Parse response
    try:
        data = response.json()
    except ValueError as e:
        raise SWAPIError(f"Failed to parse response: {e}")

    # Process response
    if resource_id:
        # Single resource
        result = data
    else:
        # Multiple resources (search or list)
        result = data.get('results', [])

    # Cache result
    if use_cache:
        _cache[cache_key] = result

    return result


def _validate_inputs(
    resource_id: Optional[int],
    search: Optional[str],
    page: Optional[int]
) -> None:
    """
    Validate input parameters for SWAPI requests.

    Args:
        resource_id: Resource ID to validate
        search: Search term to validate
        page: Page number to validate

    Raises:
        ValueError: If parameters are invalid
    """
    if resource_id is not None and resource_id <= 0:
        raise ValueError("resource_id must be positive")

    if page is not None and page <= 0:
        raise ValueError("page must be positive")

    if resource_id is not None and search is not None:
        raise ValueError("Cannot specify both resource_id and search")

    logger.debug(
        "Input validation passed: resource_id=%s, search=%s, page=%s",
        resource_id, search, page
    )


def _build_cache_key(
    resource_type: SWAPIResource,
    resource_id: Optional[int],
    search: Optional[str],
    page: Optional[int]
) -> str:
    """
    Build unique cache key from request parameters.

    Args:
        resource_type: Type of resource
        resource_id: Resource ID (if any)
        search: Search term (if any)
        page: Page number (if any)

    Returns:
        Unique cache key string

    Example:
        >>> _build_cache_key(SWAPIResource.PEOPLE, resource_id=1, search=None, page=None)
        'people|id:1'
    """
    parts = [resource_type.value]

    if resource_id:
        parts.append(f"id:{resource_id}")
    if search:
        parts.append(f"search:{search}")
    if page:
        parts.append(f"page:{page}")

    return "|".join(parts)


def _build_url(
    resource_type: SWAPIResource,
    resource_id: Optional[int],
    search: Optional[str],
    page: Optional[int]
) -> str:
    """
    Build SWAPI URL from parameters.

    Constructs the appropriate URL based on whether we're fetching:
    - A specific resource (by ID)
    - A list of resources
    - Search results
    - A specific page

    Args:
        resource_type: Type of resource to fetch
        resource_id: Specific resource ID (mutually exclusive with search)
        search: Search query string
        page: Page number for pagination

    Returns:
        Complete SWAPI URL

    Example:
        >>> _build_url(SWAPIResource.PEOPLE, resource_id=1, None, None)
        'https://swapi.dev/api/people/1/'

        >>> _build_url(SWAPIResource.PLANETS, None, "Tatooine", None)
        'https://swapi.dev/api/planets/?search=Tatooine'
    """
    base_url = "https://swapi.dev/api"
    resource_path = resource_type.value

    if resource_id:
        # Specific resource by ID
        url = f"{base_url}/{resource_path}/{resource_id}/"
        logger.debug("Built URL for resource ID: %s", url)
        return url

    # List or search endpoint
    url = f"{base_url}/{resource_path}/"
    params = []

    if search:
        params.append(f"search={search}")
    if page:
        params.append(f"page={page}")

    if params:
        url += "?" + "&".join(params)

    logger.debug("Built URL: %s", url)
    return url
