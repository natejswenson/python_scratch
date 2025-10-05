"""Unit tests for mathfun module."""
import pytest
from mathfun import add, subtract


class TestAdd:
    """Tests for add function."""

    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        assert add(2, 3) == 5
        assert add(10, 20) == 30

    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        assert add(-5, -3) == -8
        assert add(-10, -20) == -30

    def test_add_mixed_numbers(self):
        """Test adding positive and negative numbers."""
        assert add(5, -3) == 2
        assert add(-5, 3) == -2

    def test_add_zero(self):
        """Test adding with zero."""
        assert add(0, 5) == 5
        assert add(5, 0) == 5
        assert add(0, 0) == 0

    def test_add_floats(self):
        """Test adding floating point numbers."""
        assert add(2.5, 3.5) == 6.0
        assert add(1.1, 2.2) == pytest.approx(3.3)

    def test_add_large_numbers(self):
        """Test adding large numbers."""
        assert add(1000000, 2000000) == 3000000


class TestSubtract:
    """Tests for subtract function."""

    def test_subtract_positive_numbers(self):
        """Test subtracting two positive numbers."""
        assert subtract(10, 5) == 5
        assert subtract(20, 15) == 5

    def test_subtract_negative_numbers(self):
        """Test subtracting two negative numbers."""
        assert subtract(-5, -3) == -2
        assert subtract(-10, -20) == 10

    def test_subtract_mixed_numbers(self):
        """Test subtracting positive and negative numbers."""
        assert subtract(5, -3) == 8
        assert subtract(-5, 3) == -8

    def test_subtract_zero(self):
        """Test subtracting with zero."""
        assert subtract(5, 0) == 5
        assert subtract(0, 5) == -5
        assert subtract(0, 0) == 0

    def test_subtract_floats(self):
        """Test subtracting floating point numbers."""
        assert subtract(5.5, 2.5) == 3.0
        assert subtract(10.5, 3.2) == pytest.approx(7.3)

    def test_subtract_to_negative(self):
        """Test subtraction resulting in negative."""
        assert subtract(3, 5) == -2
        assert subtract(10, 20) == -10
