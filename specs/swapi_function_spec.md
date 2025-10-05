# SWAPI Python Function Specification

## 1. Overview

### 1.1 Purpose
Create a Python function that interacts with the Star Wars API (SWAPI) to retrieve and process Star Wars universe data including people, planets, starships, vehicles, species, and films.

### 1.2 Scope
- Single, well-designed function for SWAPI data retrieval
- Support for all SWAPI resource types
- Robust error handling and data validation
- Type-safe implementation with proper documentation
- Comprehensive test coverage

### 1.3 Target Users
- Developers integrating Star Wars data into applications
- Data analysts working with Star Wars universe information
- Educational projects demonstrating API integration patterns

## 2. Requirements

### 2.1 Functional Requirements

**FR1: Resource Retrieval**
- The function shall retrieve data from SWAPI endpoints
- Support resource types: people, planets, starships, vehicles, species, films
- Accept resource ID or search parameters
- Return structured data in Python-friendly format

**FR2: Search Functionality**
- Support searching by name/title across all resource types
- Handle partial matches and case-insensitive searches
- Return list of matching results

**FR3: Pagination Handling**
- Automatically handle SWAPI pagination
- Support retrieving all results or limited results
- Provide option to get specific page

**FR4: Data Processing**
- Parse JSON responses into Python dictionaries
- Resolve related resource URLs to actual data (optional)
- Cache responses to minimize API calls

**FR5: Error Handling**
- Handle network errors gracefully
- Manage HTTP error codes (404, 500, etc.)
- Validate input parameters
- Provide meaningful error messages

### 2.2 Non-Functional Requirements

**NFR1: Performance**
- Response time < 2 seconds for single resource
- Support concurrent requests for bulk operations
- Implement caching to reduce API load

**NFR2: Reliability**
- Retry logic for transient failures (max 3 retries)
- Timeout handling (10 second default)
- Graceful degradation on API unavailability

**NFR3: Maintainability**
- Type hints for all parameters and returns
- Comprehensive docstrings
- Follow PEP 8 style guidelines
- Modular design for easy extension

**NFR4: Testability**
- 100% unit test coverage
- Mockable external dependencies
- Integration tests with live API
- Performance benchmarks

## 3. TDD Plan

### 3.1 Red-Green-Refactor Cycle

**Phase 1: Basic Resource Retrieval (Red → Green → Refactor)**
1. **Red**: Write failing test for getting a person by ID
2. **Green**: Implement minimal code to pass test
3. **Refactor**: Extract common patterns, improve design

**Phase 2: Error Handling (Red → Green → Refactor)**
1. **Red**: Write tests for 404, timeout, network errors
2. **Green**: Implement error handling
3. **Refactor**: Create error handling utilities

**Phase 3: Search Functionality (Red → Green → Refactor)**
1. **Red**: Write tests for search operations
2. **Green**: Implement search logic
3. **Refactor**: Optimize search algorithm

**Phase 4: Pagination (Red → Green → Refactor)**
1. **Red**: Write tests for multi-page results
2. **Green**: Implement pagination handling
3. **Refactor**: Extract pagination logic

**Phase 5: Caching (Red → Green → Refactor)**
1. **Red**: Write tests for cache hits/misses
2. **Green**: Implement caching mechanism
3. **Refactor**: Optimize cache strategy

### 3.2 Test Categories

#### Unit Tests
- Input parameter validation
- URL construction logic
- Response parsing
- Error handling paths
- Cache operations
- Data transformation logic

#### Integration Tests
- Live API calls to SWAPI
- End-to-end resource retrieval
- Search across resource types
- Pagination with real data
- Network error simulation

#### Performance Tests
- Response time benchmarks
- Concurrent request handling
- Cache effectiveness
- Memory usage profiling

## 4. Architecture Design

### 4.1 Function Signature

```python
from typing import Optional, Dict, List, Union, Literal
from enum import Enum

class SWAPIResource(Enum):
    PEOPLE = "people"
    PLANETS = "planets"
    STARSHIPS = "starships"
    VEHICLES = "vehicles"
    SPECIES = "species"
    FILMS = "films"

def get_swapi_data(
    resource_type: SWAPIResource,
    resource_id: Optional[int] = None,
    search: Optional[str] = None,
    page: Optional[int] = None,
    resolve_urls: bool = False,
    use_cache: bool = True,
    timeout: int = 10
) -> Union[Dict, List[Dict]]:
    """
    Retrieve data from the Star Wars API (SWAPI).

    Args:
        resource_type: Type of resource to retrieve
        resource_id: Specific resource ID (optional)
        search: Search term for filtering (optional)
        page: Specific page number for pagination (optional)
        resolve_urls: Whether to resolve related resource URLs (default: False)
        use_cache: Whether to use cached responses (default: True)
        timeout: Request timeout in seconds (default: 10)

    Returns:
        Dict for single resource, List[Dict] for multiple resources

    Raises:
        ValueError: Invalid parameters
        requests.exceptions.HTTPError: HTTP error from API
        requests.exceptions.Timeout: Request timeout
        requests.exceptions.RequestException: Network error
    """
    pass
```

### 4.2 Component Structure

```
swapi.py
├── get_swapi_data()          # Main public function
├── _build_url()              # URL construction helper
├── _make_request()           # HTTP request wrapper
├── _parse_response()         # JSON parsing
├── _handle_pagination()      # Pagination logic
├── _resolve_related_urls()   # URL resolution (optional)
├── _cache_get()              # Cache retrieval
├── _cache_set()              # Cache storage
└── SWAPIError                # Custom exception class
```

### 4.3 Data Flow

```
Input Parameters
    ↓
Validate Input
    ↓
Check Cache (if enabled)
    ↓
Build Request URL
    ↓
Make HTTP Request (with retry logic)
    ↓
Parse JSON Response
    ↓
Handle Pagination (if needed)
    ↓
Resolve URLs (if requested)
    ↓
Cache Result (if enabled)
    ↓
Return Data
```

## 5. Implementation Phases

### Phase 1: Foundation (Week 1)
**Tasks:**
- [ ] Set up project structure
- [ ] Create test file structure
- [ ] Implement basic function skeleton
- [ ] Add type hints and docstrings
- [ ] Set up pytest configuration

**Tests to Write First:**
```python
def test_get_person_by_id_returns_dict()
def test_invalid_resource_type_raises_value_error()
def test_invalid_resource_id_raises_value_error()
```

**Acceptance Criteria:**
- Function signature defined with type hints
- Basic parameter validation works
- Tests pass for happy path and basic errors

### Phase 2: Core Functionality (Week 1-2)
**Tasks:**
- [ ] Implement HTTP request logic
- [ ] Add response parsing
- [ ] Implement error handling
- [ ] Add timeout support

**Tests to Write First:**
```python
def test_get_person_by_id_makes_correct_api_call()
def test_404_error_raises_http_error()
def test_timeout_raises_timeout_error()
def test_network_error_raises_request_exception()
def test_response_parsed_correctly()
```

**Acceptance Criteria:**
- Successfully retrieves single resources by ID
- All SWAPI resource types supported
- Proper error handling for HTTP errors
- Timeout mechanism works correctly

### Phase 3: Search and Pagination (Week 2)
**Tasks:**
- [ ] Implement search functionality
- [ ] Add pagination handling
- [ ] Support fetching all pages
- [ ] Add page-specific retrieval

**Tests to Write First:**
```python
def test_search_by_name_returns_list()
def test_search_with_no_results_returns_empty_list()
def test_pagination_retrieves_all_results()
def test_specific_page_retrieval()
def test_case_insensitive_search()
```

**Acceptance Criteria:**
- Search works across all resource types
- Pagination automatically handled
- Can retrieve specific pages
- Case-insensitive matching works

### Phase 4: Advanced Features (Week 3)
**Tasks:**
- [ ] Implement caching mechanism
- [ ] Add URL resolution feature
- [ ] Implement retry logic
- [ ] Add concurrent request support

**Tests to Write First:**
```python
def test_cache_hit_does_not_make_api_call()
def test_cache_miss_makes_api_call()
def test_resolve_urls_fetches_related_data()
def test_retry_logic_on_transient_failure()
def test_concurrent_requests_handled_correctly()
```

**Acceptance Criteria:**
- Caching reduces API calls by 80%
- URL resolution works for all resource types
- Retry logic handles transient failures
- Concurrent requests work without race conditions

### Phase 5: Polish and Documentation (Week 3-4)
**Tasks:**
- [ ] Add comprehensive examples
- [ ] Create usage documentation
- [ ] Performance optimization
- [ ] Code review and refactoring

**Tests to Write First:**
```python
def test_performance_single_request_under_2_seconds()
def test_performance_cached_request_under_100ms()
def test_bulk_requests_complete_within_threshold()
```

**Acceptance Criteria:**
- Documentation complete with examples
- Performance meets requirements
- Code coverage > 95%
- All edge cases handled

## 6. Testing Strategy

### 6.1 Unit Test Coverage

```python
# Test file: tests/test_swapi.py

class TestInputValidation:
    def test_valid_resource_type_accepted()
    def test_invalid_resource_type_raises_error()
    def test_negative_resource_id_raises_error()
    def test_invalid_page_number_raises_error()
    def test_conflicting_params_raises_error()

class TestURLConstruction:
    def test_url_for_resource_id()
    def test_url_for_search()
    def test_url_for_pagination()
    def test_base_url_correct()

class TestResponseParsing:
    def test_parse_single_resource()
    def test_parse_list_of_resources()
    def test_parse_empty_results()
    def test_parse_malformed_json_raises_error()

class TestErrorHandling:
    def test_404_not_found()
    def test_500_server_error()
    def test_timeout_error()
    def test_connection_error()
    def test_invalid_json_error()

class TestCaching:
    def test_cache_stores_result()
    def test_cache_retrieves_result()
    def test_cache_respects_ttl()
    def test_cache_disabled_makes_request()

class TestSearchFunctionality:
    def test_search_exact_match()
    def test_search_partial_match()
    def test_search_case_insensitive()
    def test_search_no_results()

class TestPagination:
    def test_get_all_pages()
    def test_get_specific_page()
    def test_pagination_with_search()
    def test_single_page_no_pagination()

class TestURLResolution:
    def test_resolve_single_url()
    def test_resolve_multiple_urls()
    def test_resolve_nested_urls()
    def test_resolve_disabled_returns_urls()
```

### 6.2 Integration Tests

```python
# Test file: tests/test_swapi_integration.py

class TestLiveAPI:
    @pytest.mark.integration
    def test_get_luke_skywalker()

    @pytest.mark.integration
    def test_search_for_tatooine()

    @pytest.mark.integration
    def test_get_all_films()

    @pytest.mark.integration
    def test_resolve_homeworld_url()
```

### 6.3 Test Fixtures

```python
# tests/conftest.py

@pytest.fixture
def mock_swapi_response():
    return {
        "name": "Luke Skywalker",
        "height": "172",
        "mass": "77",
        "hair_color": "blond",
        "homeworld": "https://swapi.dev/api/planets/1/"
    }

@pytest.fixture
def mock_search_response():
    return {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [{"name": "Luke Skywalker"}]
    }

@pytest.fixture
def mock_requests_get(mocker, mock_swapi_response):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_swapi_response
    return mocker.patch('requests.get', return_value=mock_response)
```

### 6.4 Mocking Strategy

- Mock all `requests.get()` calls for unit tests
- Use `responses` library for request mocking
- Create fixtures for common API responses
- Simulate error conditions with mock responses
- Use real API for integration tests only

## 7. Definition of Done

### 7.1 Code Complete Checklist
- [ ] All functions implemented
- [ ] Type hints on all functions
- [ ] Docstrings with examples
- [ ] Error handling complete
- [ ] Logging added
- [ ] Code formatted with Black
- [ ] Imports sorted with isort
- [ ] No linting errors (flake8, pylint)

### 7.2 Testing Complete Checklist
- [ ] All unit tests passing
- [ ] Test coverage > 95%
- [ ] Integration tests passing
- [ ] Performance tests passing
- [ ] Edge cases covered
- [ ] Error paths tested
- [ ] Mock coverage complete

### 7.3 Documentation Complete Checklist
- [ ] Function docstrings complete
- [ ] Usage examples provided
- [ ] README updated
- [ ] API reference documented
- [ ] Error codes documented
- [ ] Performance characteristics documented

### 7.4 Quality Gates
- [ ] Code review approved
- [ ] No security vulnerabilities
- [ ] Performance requirements met
- [ ] All acceptance criteria met
- [ ] CI/CD pipeline passing

## 8. Acceptance Criteria

### 8.1 Functional Acceptance
1. **Resource Retrieval**
   - Can retrieve any resource type by ID
   - Returns properly formatted Python dictionary
   - Handles all 6 resource types

2. **Search Functionality**
   - Search works for all resource types
   - Case-insensitive matching
   - Returns list of matching results
   - Empty list for no matches

3. **Error Handling**
   - 404 errors handled gracefully
   - Network errors raise appropriate exceptions
   - Timeouts handled properly
   - Invalid input raises ValueError

4. **Performance**
   - Single request < 2 seconds
   - Cached request < 100ms
   - Handles 10 concurrent requests

5. **Caching**
   - Cache reduces duplicate API calls
   - Cache can be disabled
   - Cache respects TTL

### 8.2 Technical Acceptance
- Type hints verified with mypy
- Code coverage ≥ 95%
- All tests pass
- No linting errors
- Documentation complete

### 8.3 User Acceptance
- Function is intuitive to use
- Error messages are clear
- Examples work as documented
- Performance is acceptable

## 9. Example Usage

### 9.1 Basic Usage

```python
from swapi import get_swapi_data, SWAPIResource

# Get a specific person
luke = get_swapi_data(SWAPIResource.PEOPLE, resource_id=1)
print(luke['name'])  # "Luke Skywalker"

# Search for a planet
tatooine = get_swapi_data(SWAPIResource.PLANETS, search="Tatooine")
print(tatooine[0]['climate'])  # "arid"

# Get all films
films = get_swapi_data(SWAPIResource.FILMS)
print(len(films))  # 6

# Get with URL resolution
luke_with_homeworld = get_swapi_data(
    SWAPIResource.PEOPLE,
    resource_id=1,
    resolve_urls=True
)
print(luke_with_homeworld['homeworld']['name'])  # "Tatooine"
```

### 9.2 Advanced Usage

```python
# Disable caching
fresh_data = get_swapi_data(
    SWAPIResource.PEOPLE,
    resource_id=1,
    use_cache=False
)

# Custom timeout
quick_request = get_swapi_data(
    SWAPIResource.PLANETS,
    search="Hoth",
    timeout=5
)

# Specific page
page_2_people = get_swapi_data(
    SWAPIResource.PEOPLE,
    page=2
)
```

## 10. Dependencies

### 10.1 Production Dependencies
```txt
requests==2.32.3
python-decouple==3.8
typing-extensions==4.12.2  # For Python < 3.11
```

### 10.2 Development Dependencies
```txt
pytest==8.3.4
pytest-cov==6.0.0
pytest-mock==3.14.0
responses==0.25.0  # HTTP mocking
black==24.10.0
mypy==1.14.0
flake8==7.1.1
```

## 11. Risk Assessment

### 11.1 Technical Risks
- **API Availability**: SWAPI may be down or slow
  - *Mitigation*: Implement robust retry logic and caching

- **API Changes**: SWAPI schema might change
  - *Mitigation*: Version schema validation, graceful degradation

- **Rate Limiting**: SWAPI may implement rate limits
  - *Mitigation*: Implement exponential backoff, request throttling

### 11.2 Schedule Risks
- **Complexity Underestimation**: Features may take longer
  - *Mitigation*: Prioritize core features first, advanced features optional

- **Testing Overhead**: Comprehensive testing takes time
  - *Mitigation*: Parallel test development with TDD approach

## 12. Success Metrics

### 12.1 Quality Metrics
- Code coverage ≥ 95%
- Zero critical bugs
- All acceptance tests passing
- Performance benchmarks met

### 12.2 Usage Metrics
- Function successfully retrieves all resource types
- Error rate < 1% for valid requests
- Cache hit rate > 70%
- Average response time < 1 second

### 12.3 Maintainability Metrics
- Cyclomatic complexity < 10 per function
- Documentation coverage 100%
- No code duplication > 5 lines
- Type coverage 100%

## 13. Timeline

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| Phase 1: Foundation | 2 days | Project setup, basic structure, initial tests |
| Phase 2: Core Functionality | 3 days | Resource retrieval, error handling |
| Phase 3: Search & Pagination | 3 days | Search, pagination implementation |
| Phase 4: Advanced Features | 4 days | Caching, URL resolution, retry logic |
| Phase 5: Polish | 2 days | Documentation, optimization, review |
| **Total** | **14 days** | **Production-ready SWAPI function** |

## 14. Appendix

### 14.1 SWAPI Endpoints
- People: https://swapi.dev/api/people/
- Planets: https://swapi.dev/api/planets/
- Films: https://swapi.dev/api/films/
- Species: https://swapi.dev/api/species/
- Vehicles: https://swapi.dev/api/vehicles/
- Starships: https://swapi.dev/api/starships/

### 14.2 Example API Responses
See: https://swapi.dev/documentation

### 14.3 Related Documentation
- SWAPI Documentation: https://swapi.dev/documentation
- Requests Library: https://requests.readthedocs.io/
- Python Type Hints: https://docs.python.org/3/library/typing.html
