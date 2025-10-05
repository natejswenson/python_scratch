"""Manual test runner for SWAPI module to verify TDD implementation."""
import sys
from unittest.mock import Mock, patch

# Mock requests module before importing swapi
sys.modules['requests'] = Mock()

from swapi import get_swapi_data, SWAPIResource, SWAPIError

def test_validation():
    """Test input validation."""
    print("Testing input validation...")

    # Test negative resource_id
    try:
        get_swapi_data(SWAPIResource.PEOPLE, resource_id=-1)
        print("  ✗ FAIL: Should reject negative resource_id")
        return False
    except ValueError as e:
        if "resource_id must be positive" in str(e):
            print("  ✓ PASS: Rejects negative resource_id")
        else:
            print(f"  ✗ FAIL: Wrong error message: {e}")
            return False

    # Test zero resource_id
    try:
        get_swapi_data(SWAPIResource.PEOPLE, resource_id=0)
        print("  ✗ FAIL: Should reject zero resource_id")
        return False
    except ValueError as e:
        if "resource_id must be positive" in str(e):
            print("  ✓ PASS: Rejects zero resource_id")
        else:
            print(f"  ✗ FAIL: Wrong error message: {e}")
            return False

    # Test conflicting params
    try:
        get_swapi_data(SWAPIResource.PEOPLE, resource_id=1, search="Luke")
        print("  ✗ FAIL: Should reject resource_id and search together")
        return False
    except ValueError as e:
        if "Cannot specify both" in str(e):
            print("  ✓ PASS: Rejects conflicting parameters")
        else:
            print(f"  ✗ FAIL: Wrong error message: {e}")
            return False

    return True

def test_url_construction():
    """Test URL construction."""
    print("\nTesting URL construction...")

    with patch('swapi.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"name": "Luke"}

        # Test resource by ID
        get_swapi_data(SWAPIResource.PEOPLE, resource_id=1)
        url = mock_get.call_args[0][0]

        if "https://swapi.dev/api/people/1/" == url:
            print("  ✓ PASS: Correct URL for resource ID")
        else:
            print(f"  ✗ FAIL: Wrong URL: {url}")
            return False

        # Test search
        mock_get.reset_mock()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"count": 1, "results": [{"name": "Luke"}]}

        get_swapi_data(SWAPIResource.PLANETS, search="Tatooine")
        url = mock_get.call_args[0][0]

        if "planets/" in url and "search=Tatooine" in url:
            print("  ✓ PASS: Correct URL for search")
        else:
            print(f"  ✗ FAIL: Wrong search URL: {url}")
            return False

    return True

def test_response_parsing():
    """Test response parsing."""
    print("\nTesting response parsing...")

    # Clear cache before testing
    from swapi import _cache
    _cache.clear()

    with patch('swapi.requests.get') as mock_get:
        # Test single resource
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "name": "Luke Skywalker",
            "height": "172"
        }

        result = get_swapi_data(SWAPIResource.PEOPLE, resource_id=1)

        if isinstance(result, dict) and result["name"] == "Luke Skywalker":
            print("  ✓ PASS: Parses single resource correctly")
        else:
            print(f"  ✗ FAIL: Wrong parse result: {result}")
            return False

        # Test list of resources
        mock_get.return_value.json.return_value = {
            "count": 2,
            "results": [
                {"name": "Luke"},
                {"name": "Leia"}
            ]
        }

        result = get_swapi_data(SWAPIResource.PEOPLE, search="L")

        if isinstance(result, list) and len(result) == 2:
            print("  ✓ PASS: Parses list of resources correctly")
        else:
            print(f"  ✗ FAIL: Wrong list result: {result}")
            return False

    return True

def test_error_handling():
    """Test error handling."""
    print("\nTesting error handling...")

    # Clear cache before testing
    from swapi import _cache
    _cache.clear()

    # Create mock exception classes
    class MockHTTPError(Exception):
        pass

    class MockTimeout(Exception):
        pass

    with patch('swapi.requests.get') as mock_get:
        # Patch the exception classes
        with patch('swapi.requests.exceptions.HTTPError', MockHTTPError):
            with patch('swapi.requests.exceptions.Timeout', MockTimeout):
                # Test 404
                mock_get.return_value.status_code = 404
                mock_get.return_value.raise_for_status.side_effect = MockHTTPError("Not found")

                try:
                    get_swapi_data(SWAPIResource.PEOPLE, resource_id=9999)
                    print("  ✗ FAIL: Should raise SWAPIError for 404")
                    return False
                except SWAPIError as e:
                    if "Resource not found" in str(e):
                        print("  ✓ PASS: Handles 404 correctly")
                    else:
                        print(f"  ✗ FAIL: Wrong 404 error: {e}")
                        return False

                # Test timeout
                mock_get.side_effect = MockTimeout("Timeout")

                try:
                    get_swapi_data(SWAPIResource.PEOPLE, resource_id=1)
                    print("  ✗ FAIL: Should raise SWAPIError for timeout")
                    return False
                except SWAPIError as e:
                    if "timeout" in str(e).lower():
                        print("  ✓ PASS: Handles timeout correctly")
                    else:
                        print(f"  ✗ FAIL: Wrong timeout error: {e}")
                        return False

    return True

def test_caching():
    """Test caching functionality."""
    print("\nTesting caching...")

    # Clear cache before testing
    from swapi import _cache
    _cache.clear()

    with patch('swapi.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"name": "Luke"}

        # First call
        result1 = get_swapi_data(SWAPIResource.PEOPLE, resource_id=1, use_cache=True)
        # Second call should use cache
        result2 = get_swapi_data(SWAPIResource.PEOPLE, resource_id=1, use_cache=True)

        if mock_get.call_count == 1:
            print("  ✓ PASS: Caching works (only 1 API call)")
        else:
            print(f"  ✗ FAIL: Made {mock_get.call_count} API calls instead of 1")
            return False

        # Test cache disabled
        mock_get.reset_mock()
        get_swapi_data(SWAPIResource.PEOPLE, resource_id=2, use_cache=False)
        get_swapi_data(SWAPIResource.PEOPLE, resource_id=2, use_cache=False)

        if mock_get.call_count == 2:
            print("  ✓ PASS: Cache can be disabled (2 API calls)")
        else:
            print(f"  ✗ FAIL: Made {mock_get.call_count} API calls instead of 2")
            return False

    return True

def test_timeout_config():
    """Test timeout configuration."""
    print("\nTesting timeout configuration...")

    # Clear cache before testing
    from swapi import _cache
    _cache.clear()

    with patch('swapi.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"name": "Luke"}

        # Test custom timeout
        get_swapi_data(SWAPIResource.PEOPLE, resource_id=1, timeout=5)

        if mock_get.call_args and mock_get.call_args.kwargs.get('timeout') == 5:
            print("  ✓ PASS: Custom timeout used")
        elif mock_get.call_args:
            print(f"  ✗ FAIL: Wrong timeout: {mock_get.call_args}")
            return False
        else:
            print("  ✗ FAIL: mock_get was not called")
            return False

        # Test default timeout
        mock_get.reset_mock()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"name": "Leia"}
        # Use different ID to avoid cache
        get_swapi_data(SWAPIResource.PEOPLE, resource_id=2)

        if mock_get.call_args and mock_get.call_args.kwargs.get('timeout') == 10:
            print("  ✓ PASS: Default timeout used (10)")
        elif mock_get.call_args:
            print(f"  ✗ FAIL: Wrong default timeout: {mock_get.call_args}")
            return False
        else:
            print("  ✗ FAIL: mock_get was not called")
            return False

    return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("SWAPI TDD VERIFICATION - Manual Test Runner")
    print("=" * 60)

    tests = [
        ("Input Validation", test_validation),
        ("URL Construction", test_url_construction),
        ("Response Parsing", test_response_parsing),
        ("Error Handling", test_error_handling),
        ("Caching", test_caching),
        ("Timeout Configuration", test_timeout_config),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n  ✗ EXCEPTION in {test_name}: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")

    total = len(results)
    passed = sum(1 for _, p in results if p)

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED - TDD CYCLE COMPLETE!")
        return 0
    else:
        print(f"\n❌ {total - passed} tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
