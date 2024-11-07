"""Unit tests for the Calculation class in the app.calculation module."""

from unittest.mock import patch
from app.operations import Add, Subtract
from app.calculation import Calculation


def test_calculation_initialization():
    """Test initialization of Calculation class."""
    add_operation = Add()  # Create an instance of Add
    calc = Calculation(operation=add_operation, operand1=5, operand2=3)
    assert calc.operation == add_operation
    assert calc.operand1 == 5
    assert calc.operand2 == 3


def test_calculation_str():
    """Test the __str__ method."""
    add_operation = Add()  # Create an instance of Add
    calc = Calculation(operation=add_operation, operand1=5, operand2=3)

    # Directly call the calculate method
    result = calc.operation.calculate(calc.operand1, calc.operand2)

    expected_result = f"5 {add_operation} 3 = {result}"
    assert str(calc) == expected_result


def test_calculation_repr():
    """Test the __repr__ method."""
    add_operation = Add()  # Create an instance of Add
    calc = Calculation(operation=add_operation, operand1=5, operand2=3)

    expected_repr = f"Calculation({add_operation}, 5, 3)"
    assert repr(calc) == expected_repr, "The __repr__ method did not return the expected string."


# Test cases to cover the perform_operation method

@patch.object(Add, 'calculate', return_value=8)  # Mock the calculate method of Add
def test_perform_operation_add(mock_calculate):
    """Test perform_operation for the Add operation."""
    add_operation = Add()  # Create an instance of Add
    calc = Calculation(operation=add_operation, operand1=5, operand2=3)

    # Perform the operation
    result = calc.perform_operation()

    # Check that the calculate method was called correctly
    mock_calculate.assert_called_once_with(5, 3)  # Assert that calculate was called with 5 and 3

    # Check that the result is correct
    assert result == 8  # The mock value for the calculate method is 8


@patch.object(Subtract, 'calculate', return_value=2)  # Mock the calculate method of Subtract
def test_perform_operation_subtract(mock_calculate):
    """Test perform_operation for the Subtract operation."""
    subtract_operation = Subtract()  # Create an instance of Subtract
    calc = Calculation(operation=subtract_operation, operand1=5, operand2=3)

    # Perform the operation
    result = calc.perform_operation()

    # Check that the calculate method was called correctly
    mock_calculate.assert_called_once_with(5, 3)  # Assert that calculate was called with 5 and 3

    # Check that the result is correct
    assert result == 2  # The mock value for the calculate method is 2
