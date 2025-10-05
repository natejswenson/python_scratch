"""Basic mathematical utility functions."""
from typing import Union

Number = Union[int, float]

def add(x: Number, y: Number) -> Number:
    """Add two numbers and return the result."""
    result = x + y
    print(f"{x} + {y} = {result}")
    return result

def subtract(x: Number, y: Number) -> Number:
    """Subtract y from x and return the result."""
    result = x - y
    print(f"{x} - {y} = {result}")
    return result

def main() -> None:
    """Main function to demonstrate the math functions."""
    add(99, 1)
    add(200, 300)
    add(5, 1)
    subtract(10, 5)

if __name__ == "__main__":
    main()
