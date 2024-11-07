import logging
from unittest.mock import patch, call, MagicMock, PropertyMock
import pytest
import pandas as pd

from app.calculator import calculator
from app.operations import Add, Subtract, Multiply, Divide

@pytest.fixture(autouse=True)
def set_test_mode(monkeypatch):
    """Fixture to set TEST_MODE to 'True' during tests."""
    monkeypatch.setenv("TEST_MODE", "True")
    yield
    # After the test, TEST_MODE will be reset to its original value automatically

@pytest.mark.parametrize(
    "operation_class, operand1, operand2, expected_result",
    [
        (Add, 2.0, 3.0, 5.0),
        (Subtract, 5.0, 3.0, 2.0),
        (Multiply, 2.0, 3.0, 6.0),
        (Divide, 6.0, 2.0, 3.0),
    ]
)
def test_operations(operation_class, operand1, operand2, expected_result, caplog):
    """Test various arithmetic operations and ensure no logs are generated."""
    with caplog.at_level(logging.CRITICAL):
        operation = operation_class()
        result = operation.calculate(operand1, operand2)
        assert result == expected_result
    assert len(caplog.records) == 0

def test_divide_by_zero(caplog):
    """Test dividing by zero raises an exception and ensure no logs are generated."""
    operation = Divide()
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        with caplog.at_level(logging.CRITICAL):
            operation.calculate(6.0, 0.0)
    assert len(caplog.records) == 0

def test_invalid_input(caplog):
    """Test invalid input raises a ValueError and ensure no logs are generated."""
    operation = Add()
    with pytest.raises(ValueError, match="Both inputs must be numbers."):
        with caplog.at_level(logging.CRITICAL):
            operation.calculate("two", 3.0)
    assert len(caplog.records) == 0

@patch('builtins.input', side_effect=["help", "exit"])
@patch("builtins.print")
def test_help_command(mock_print, caplog):
    """Test that the help command displays the correct information and exits correctly."""
    with caplog.at_level(logging.CRITICAL):
        calculator()
    mock_print.assert_any_call("Available commands:")
    mock_print.assert_any_call("    ✶ add      <num1> <num2>    : Adds two numbers.")
    mock_print.assert_any_call("    ✶ subtract <num1> <num2>    : Subtracts two numbers.")
    mock_print.assert_any_call("    ✶ multiply <num1> <num2>    : Multiplies two numbers.")
    mock_print.assert_any_call("    ✶ divide   <num1> <num2>    : Divides two numbers.")
    mock_print.assert_any_call("    ✶ list                      : Shows operation history.")
    mock_print.assert_any_call("    ✶ undo                      : Removes last operation from history.")
    mock_print.assert_any_call("    ✶ exit                      : Exits the calculator.")
    mock_print.assert_any_call("Exiting calculator...")
    assert len(caplog.records) == 0

@patch('builtins.input', side_effect=["exit"])
@patch("builtins.print")
@patch("app.history_manager.History._instance", new_callable=PropertyMock)
def test_exit_command(mock_input, mock_print, mock_history_instance, caplog):
    """Test that the calculator exits correctly after 'exit' command."""
    mock_history_instance.return_value = MagicMock()
    with caplog.at_level(logging.CRITICAL):
        calculator()
    mock_print.assert_any_call("Exiting calculator...")
    assert len(caplog.records) == 0

@pytest.mark.parametrize(
    "operation_class, operand1, operand2, result",
    [
        (Add, 1, 2, 3),
        (Subtract, 5, 3, 2),
        (Multiply, 3, 4, 12),
        (Divide, 8, 2, 4),
    ]
)
def test_calculator_valid_operations(operation_class, operand1, operand2, result):
    """Test that the calculator handles valid operations and inputs correctly."""
    with patch('builtins.print') as mock_print, \
         patch('builtins.input', side_effect=[
             'add 3 4', 
             'subtract 5 2', 
             'multiply 3 3', 
             'divide 6 2', 
             'exit'
         ]), \
         patch('builtins.open', MagicMock()), \
         patch.object(pd, 'read_csv', return_value=pd.DataFrame(columns=["Operation", "Operand #1", "Operand #2", "Result"])):
        
        calculator()
        
        mock_print.assert_any_call("Result: 7.0")
        mock_print.assert_any_call("Result: 3.0")
        mock_print.assert_any_call("Result: 9.0")
        mock_print.assert_any_call("Result: 3.0")
        mock_print.assert_any_call("Exiting calculator...")


@patch('builtins.input', side_effect=[
    'add abc 2',  # Invalid input
    'multiply 3 four',  # Invalid input
    'divide 8 0',  # Invalid input
    'exit'  # Exit command
])
@patch('builtins.print')
def test_various_invalid_inputs(mock_print, _mock_input):
    """Test handling of various invalid inputs in the calculator."""
    calculator()

    # The invalid message that should be shown for each invalid input
    invalid_message = (
        "Invalid input. Please enter a valid operation and two numbers. "
        "Type 'help' for instructions."
    )

    # Check that the invalid input message is printed for each invalid input
    mock_print.assert_any_call(invalid_message)
    mock_print.assert_any_call(invalid_message)
    mock_print.assert_any_call(invalid_message)

    # Ensure that the exit message is printed at the end
    mock_print.assert_any_call("Exiting calculator...")

    # Define the expected order of calls **without** the tuple wrapping
    expected_calls = [
        "Welcome to the calculator! Type 'help' for a list of commands.",
        invalid_message,
        invalid_message,
        invalid_message,
        "Exiting calculator..."
    ]

    # Ensure the calls are in the correct order and match exactly
    mock_print.assert_has_calls([call(expected) for expected in expected_calls], any_order=False)
