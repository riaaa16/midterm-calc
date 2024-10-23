'''
Testing operations with paramterized tests
'''

import pytest
from app.operations import add, subtract, multiply, divide

@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),         # positive numbers
    (-1, -2, -3),     # negative numbers
    (0, 0, 0),        # zero
    (1.5, 2.5, 4.0),  # float
    (1e10, 1e10, 2e10) # large numbers
])
def test_addition(a, b, expected):
    """
    Test the add function with various inputs.

    Parameters:
    a (float): First number to add.
    b (float): Second number to add.
    expected (float): Expected result of the addition.
    """
    assert add(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
    (3, 2, 1),         # positive numbers
    (-1, -2, 1),      # negative numbers
    (0, 0, 0),        # zero
    (1.5, 2.5, -1.0),  # float
    (1e10, 1e10, 0)    # large numbers
])
def test_subtraction(a, b, expected):
    """
    Test the subtract function with various inputs.

    Parameters:
    a (float): Number from which to subtract.
    b (float): Number to subtract.
    expected (float): Expected result of the subtraction.
    """
    assert subtract(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
    (2, 5, 10),       # positive numbers
    (-1, -1, 1),     # negative numbers
    (0, 5, 0),       # zero
    (1.5, 2, 3.0),   # float
    (1e10, 0, 0)     # boundary case
])
def test_multiplication(a, b, expected):
    """
    Test the multiply function with various inputs.

    Parameters:
    a (float): First number to multiply.
    b (float): Second number to multiply.
    expected (float): Expected result of the multiplication.
    """
    assert multiply(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5),              # positive numbers
    (-10, -2, 5),            # negative numbers
    (0, 1, 0),               # zero
    (1.5, 0.5, 3.0),         # float
    (1e10, 1e10, 1),         # large numbers
])
def test_division(a, b, expected):
    """
    Test the divide function with various inputs.

    Parameters:
    a (float): Numerator.
    b (float): Denominator.
    expected (float): Expected result of the division.
    """
    assert divide(a, b) == expected

def test_division_by_zero():
    """
    Test that dividing by zero raises a ValueError.

    This test checks that the divide function correctly raises
    a ValueError when the denominator is zero.
    """
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        divide(10, 0)
