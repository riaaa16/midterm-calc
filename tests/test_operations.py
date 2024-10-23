'''
Testing operations with parameterized tests
'''

import pytest
from app.operations import Add, Subtract, Multiply, Divide

# Parameterized tests for addition
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),                 # positive numbers
    (-1, -2, -3),             # negative numbers
    (0, 0, 0),                # zero
    (1.5, 2.5, 4.0),          # float
    (1e10, 1e10, 2e10),       # large numbers
    ('abc', 2, ValueError),   # invalid input (string)
    (1, 'abc', ValueError),   # invalid input (string)
    (None, 2, ValueError),     # invalid input (None)
])
def test_addition(a, b, expected):
    """Test the Add operation."""
    operation = Add()
    if expected is ValueError:
        with pytest.raises(ValueError):
            operation.calculate(a, b)
    else:
        assert operation.calculate(a, b) == expected

# Parameterized tests for subtraction
@pytest.mark.parametrize("a, b, expected", [
    (3, 2, 1),                 # positive numbers
    (-1, -2, 1),              # negative numbers
    (0, 0, 0),                # zero
    (1.5, 2.5, -1.0),         # float
    (1e10, 1e10, 0),          # large numbers
    ('abc', 2, ValueError),   # invalid input (string)
    (1, 'abc', ValueError),   # invalid input (string)
    (None, 2, ValueError),     # invalid input (None)
])
def test_subtraction(a, b, expected):
    """Test the Subtract operation."""
    operation = Subtract()
    if expected is ValueError:
        with pytest.raises(ValueError):
            operation.calculate(a, b)
    else:
        assert operation.calculate(a, b) == expected

# Parameterized tests for multiplication
@pytest.mark.parametrize("a, b, expected", [
    (2, 5, 10),               # positive numbers
    (-1, -1, 1),             # negative numbers
    (0, 5, 0),               # zero
    (1.5, 2, 3.0),           # float
    (1e10, 0, 0),            # boundary case
    ('abc', 2, ValueError),   # invalid input (string)
    (1, 'abc', ValueError),   # invalid input (string)
    (None, 2, ValueError),     # invalid input (None)
])
def test_multiplication(a, b, expected):
    """Test the Multiply operation."""
    operation = Multiply()
    if expected is ValueError:
        with pytest.raises(ValueError):
            operation.calculate(a, b)
    else:
        assert operation.calculate(a, b) == expected

# Parameterized tests for division
@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5),                # positive numbers
    (-10, -2, 5),              # negative numbers
    (0, 1, 0),                 # zero
    (1.5, 0.5, 3.0),           # float
    (1e10, 1e10, 1),           # large numbers
    ('abc', 2, ValueError),    # invalid input (string)
    (1, 'abc', ValueError),    # invalid input (string)
    (None, 2, ValueError),      # invalid input (None)
])
def test_division(a, b, expected):
    """Test the Divide operation."""
    operation = Divide()
    if expected is ValueError:
        with pytest.raises(ValueError):
            operation.calculate(a, b)
    else:
        assert operation.calculate(a, b) == expected

# Test for division by zero
def test_division_by_zero():
    """Test that dividing by zero raises a ValueError."""
    operation = Divide()
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        operation.calculate(10, 0)
