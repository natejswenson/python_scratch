# Unit Tests

This directory contains comprehensive unit tests for the python_fun project.

## Test Structure

```
tests/
├── __init__.py              # Package initialization
├── conftest.py              # Pytest fixtures and configuration
├── test_mathfun.py          # Tests for mathfun.py
├── test_weather.py          # Tests for weather.py
├── test_github.py           # Tests for github.py
├── test_getips.py           # Tests for getips.py (Roku discovery)
├── test_swensonRoku.py      # Tests for swensonRoku.py
├── test_smartthings.py      # Tests for smartthings.py
├── test_openai.py           # Tests for openAI.py
├── test_create_repo.py      # Tests for github/create_repo.py
└── test_reuse_requests.py   # Tests for utils/reuse_requests.py
```

## Running Tests

### Install Test Dependencies

```bash
pip install -r requirements-dev.txt
```

### Run All Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=. --cov-report=html --cov-report=term-missing
```

### Run Specific Test File

```bash
pytest tests/test_mathfun.py
```

### Run Specific Test Class or Function

```bash
pytest tests/test_mathfun.py::TestAdd
pytest tests/test_mathfun.py::TestAdd::test_add_positive_numbers
```

### Run Tests by Marker

```bash
# Run only async tests
pytest -m asyncio

# Run only unit tests
pytest -m unit

# Skip slow tests
pytest -m "not slow"
```

### Verbose Output

```bash
pytest -v
pytest -vv  # Extra verbose
```

## Test Coverage

After running tests with coverage, view the HTML report:

```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Writing New Tests

1. Create a new test file: `test_<module_name>.py`
2. Import the module to test
3. Create test classes inheriting from appropriate base
4. Write test methods starting with `test_`

Example:

```python
import pytest
from my_module import my_function

class TestMyFunction:
    def test_success_case(self):
        result = my_function(valid_input)
        assert result == expected_output

    def test_error_case(self):
        with pytest.raises(ValueError):
            my_function(invalid_input)
```

## Fixtures

Common fixtures are available in `conftest.py`:

- `mock_response` - Mock HTTP response
- `mock_api_headers` - Mock API headers
- `sample_github_repo_data` - Sample GitHub data
- `sample_weather_data` - Sample weather data
- `sample_ip_data` - Sample IP geolocation data
- `sample_smartthings_devices` - Sample SmartThings devices
- `sample_roku_apps` - Sample Roku apps
- `mock_openai_response` - Mock OpenAI response

## Test Categories

Tests are organized by module:

- **Unit Tests**: Test individual functions in isolation
- **Integration Tests**: Test interaction between components (marked with `@pytest.mark.integration`)
- **Async Tests**: Test async functions (marked with `@pytest.mark.asyncio`)

## Mocking External Dependencies

All tests use mocks for external API calls to ensure:
- Tests run quickly
- No network dependencies
- No API key requirements
- Deterministic results

Example:
```python
@patch('module.requests.get')
def test_api_call(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'key': 'value'}
    # Test code here
```

## Continuous Integration

Tests can be integrated with CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    pytest --cov=. --cov-report=xml
```
