'''
Test file to test basic app.calculation method
'''
import pytest
from app.calculation import Calculation
from app.operations import Add, Subtract, Multiply, Divide


@pytest.mark.parametrize(
    "operation, operand1, operand2, expected",
    [
        (Add(), 5, 3, 8),           # Test addition
        (Subtract(), 5, 3, 2),      # Test subtraction
        (Multiply(), 5, 3, 15),     # Test multiplication
        (Divide(), 6, 2, 3),        # Test division
    ]
)
def test_perform_operation_success(operation, operand1, operand2, expected):
    """
    Test successful execution of arithmetic operations in Calculation.

    Parameters:
    operation (OperationTemplate): The operation to test.
    operand1 (float): The first operand.
    operand2 (float): The second operand.
    expected (float): The expected result.
    """
    calc = Calculation()
    result = calc.perform_operation(operation, operand1, operand2)
    assert result == expected


def test_perform_operation_divide_by_zero():
    """
    Test division by zero case in Calculation, which should raise ValueError.
    """
    calc = Calculation()
    with pytest.raises(ValueError) as excinfo:
        calc.perform_operation(Divide(), 5, 0)
    assert str(excinfo.value) == "Cannot divide by zero."
