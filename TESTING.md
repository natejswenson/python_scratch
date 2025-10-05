# Testing Documentation

## Overview

This document provides a comprehensive overview of the testing infrastructure for the python_fun project.

## Test Coverage Summary

### Modules Tested

| Module | Test File | Test Count | Coverage Areas |
|--------|-----------|------------|----------------|
| `mathfun.py` | `test_mathfun.py` | 12 tests | Addition, subtraction, edge cases |
| `weather.py` | `test_weather.py` | 14 tests | API calls, error handling, data parsing |
| `github.py` | `test_github.py` | 6 tests | Repository info, authentication, errors |
| `getips.py` | `test_getips.py` | 6 tests | SSDP discovery, filtering, duplicates |
| `swensonRoku.py` | `test_swensonRoku.py` | 8 tests | App selection, launching, navigation |
| `smartthings.py` | `test_smartthings.py` | 4 tests | Device listing, async operations |
| `openAI.py` | `test_openai.py` | 4 tests | API calls, responses, error handling |
| `github/create_repo.py` | `test_create_repo.py` | 6 tests | Repo creation, permissions, errors |
| `utils/reuse_requests.py` | `test_reuse_requests.py` | 11 tests | HTTP methods, session management |

**Total: 71+ unit tests**

## Quick Start

### 1. Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development/testing dependencies
pip install -r requirements-dev.txt
```

### 2. Run Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=term-missing --cov-report=html

# Run specific test file
pytest tests/test_mathfun.py

# Run with verbose output
pytest -v
```

### 3. View Coverage Report

```bash
# Generate HTML coverage report
pytest --cov=. --cov-report=html

# Open the report (varies by OS)
open htmlcov/index.html        # macOS
xdg-open htmlcov/index.html    # Linux
start htmlcov/index.html       # Windows
```

## Test Categories

### Unit Tests
- Test individual functions in isolation
- Use mocks for external dependencies
- Fast execution (<1s per test)
- No network or API calls

### Async Tests
- Marked with `@pytest.mark.asyncio`
- Test async/await functions
- Examples: SmartThings API tests

### Integration Tests
- Marked with `@pytest.mark.integration`
- Test multiple components together
- Can be skipped with `-m "not integration"`

## Testing Patterns

### 1. Mocking HTTP Requests

```python
@patch('module.requests.get')
def test_api_call(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'key': 'value'}
    mock_get.return_value = mock_response

    result = function_under_test()
    assert result is not None
```

### 2. Testing Error Handling

```python
@patch('module.requests.get')
def test_network_error(mock_get):
    mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

    result = function_under_test()
    assert result is None  # Verify graceful handling
```

### 3. Testing Async Functions

```python
@pytest.mark.asyncio
@patch('module.aiohttp.ClientSession')
async def test_async_function(mock_session):
    mock_api = AsyncMock()
    mock_api.devices.return_value = [mock_device]

    result = await async_function()
    assert len(result) > 0
```

### 4. Using Fixtures

```python
def test_with_fixture(sample_github_repo_data):
    # Use pre-configured test data from conftest.py
    assert sample_github_repo_data['name'] == 'test-repo'
```

## Configuration Files

### pytest.ini
- Test discovery patterns
- Coverage settings
- Test markers
- Output formatting

### .coveragerc
- Coverage exclusions
- Report formatting
- HTML report settings

### conftest.py
- Shared fixtures
- Test setup/teardown
- Environment configuration

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt

    - name: Run tests with coverage
      run: |
        pytest --cov=. --cov-report=xml --cov-report=term-missing

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

## Best Practices

### 1. Test Naming
- Test files: `test_<module_name>.py`
- Test classes: `Test<ClassName>`
- Test functions: `test_<what_is_being_tested>`

### 2. Test Organization
- Group related tests in classes
- One assertion focus per test
- Clear, descriptive test names

### 3. Mocking
- Mock external dependencies (API calls, file I/O)
- Don't mock the code under test
- Use specific mocks (not catch-all)

### 4. Coverage Goals
- Aim for >80% coverage
- Focus on critical paths
- Test edge cases and errors

### 5. Test Maintenance
- Update tests when code changes
- Remove obsolete tests
- Keep tests simple and readable

## Common Commands

```bash
# Run tests matching pattern
pytest -k "test_add"

# Run tests and stop at first failure
pytest -x

# Run tests with pdb debugger on failure
pytest --pdb

# Run tests in parallel (requires pytest-xdist)
pytest -n auto

# Show test durations
pytest --durations=10

# Run only failed tests from last run
pytest --lf

# Run failed tests first, then others
pytest --ff
```

## Troubleshooting

### Import Errors
```bash
# Ensure you're in the project root
cd /path/to/python_fun

# Install in editable mode
pip install -e .
```

### Mock Not Working
- Verify the patch path matches the import path
- Use `where='module.function'` syntax
- Check that mocks are applied before function calls

### Async Test Failures
- Ensure `pytest-asyncio` is installed
- Mark tests with `@pytest.mark.asyncio`
- Use `AsyncMock` for async functions

### Coverage Not Accurate
- Check `.coveragerc` exclusions
- Ensure tests actually call the code
- Verify no duplicate coverage runs

## Adding New Tests

1. **Create test file**: `tests/test_<module>.py`

2. **Import required modules**:
   ```python
   import pytest
   from unittest.mock import patch, Mock
   from module import function_to_test
   ```

3. **Write test class**:
   ```python
   class TestFunctionName:
       def test_success_case(self):
           # Test code
           assert True
   ```

4. **Run new tests**:
   ```bash
   pytest tests/test_<module>.py -v
   ```

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
