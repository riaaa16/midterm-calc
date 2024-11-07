"""
Tests for the History class. Tests include 
adding operations to history, undoing operations, and printing the history 
without interacting with files. Checks the counter updates as
appropriate.
"""

from unittest.mock import patch, MagicMock
import pytest
import pandas as pd
from app.history_manager import History
from app.operations import Add, Subtract, Multiply, Divide


# Test for add_to_history with no file-writing interaction
@pytest.mark.parametrize(
    "operation_class, operand1, operand2, result",
    [
        (Add, 1, 2, 3),  # Test addition
        (Subtract, 5, 3, 2),  # Test subtraction
        (Multiply, 3, 4, 12),  # Test multiplication
        (Divide, 8, 2, 4),  # Test division
    ]
)
def test_add_to_history(operation_class, operand1, operand2, result):
    """
    Test the add_to_history method on the History class for various arithmetic operations.
    """
    # Reset the History singleton instance before each test
    History._instance = None

    # Create a new History instance for each test
    history = History()

    # Mock file-writing methods (open) to avoid file operations
    with patch('builtins.open', MagicMock()), \
         patch.object(
             pd,
             'read_csv',
             return_value=pd.DataFrame(columns=["Operation", "Operand #1", "Operand #2", "Result"])
        ):

        # Add the operation to history
        operation = operation_class()
        history.add_to_history(operation, operand1, operand2, result)

        # Assert that the counter is incremented correctly
        assert history.counter == 1  # Counter should be 1 after one operation

        # Add another operation to history
        history.add_to_history(operation, operand1, operand2, result)

        # Assert the counter is incremented correctly
        assert history.counter == 2  # Counter should be 2 after two operations

        # Add another operation to history
        history.add_to_history(operation, operand1, operand2, result)

        # Assert the counter is incremented correctly
        assert history.counter == 3  # Counter should be 3 after three operations


def test_undo_last():
    """Test the undo_last method without file interaction."""
    # Reset the History singleton instance before each test
    History._instance = None

    # Create a new History instance for each test
    history = History()

    # Mock file-writing methods (open) to avoid file operations
    with patch('builtins.open', MagicMock()), \
         patch.object(pd, 'read_csv', return_value=pd.DataFrame({
             "Operation": ["Add"],
             "Operand #1": [5],
             "Operand #2": [3],
             "Result": [8]
         })):  # Simulate a DataFrame with one row of data

        # Add an operation to history
        mock_operation = Add()
        history.add_to_history(mock_operation, 5, 3, 8)

        # Assert the counter is correct after the first operation
        assert history.counter == 1

        # Undo the last operation
        history.undo_last()

        # Assert the counter is decremented after undo
        assert history.counter == 0  # Counter should be 0 after undoing


def test_print_history():
    """Test printing the history without file writing."""
    # Reset the History singleton instance before each test
    History._instance = None

    # Create a new History instance for each test
    history = History()

    # Mock file-writing methods (open) to avoid file operations
    with patch('builtins.open', MagicMock()), \
         patch.object(pd,
            'read_csv',
            return_value=pd.DataFrame(columns=["Operation", "Operand #1", "Operand #2", "Result"])
        ), \
         patch('builtins.print') as mock_print:

        # Add some operations to history
        mock_operation1 = Add()
        history.add_to_history(mock_operation1, 5, 3, 8)

        mock_operation2 = Subtract()
        history.add_to_history(mock_operation2, 10, 5, 5)

        # Mock the DataFrame's to_string method to return a controlled output
        with patch.object(pd.DataFrame, 'to_string', return_value=(
            "   Operation  Operand #1  Operand #2  Result\n"
            "37       Add           5           3       8\n"
            "38  Subtract          10           5       5"
        )) as mock_to_string:
            # Print the history
            history.print_history()

            # Assert that print was called with the expected string
            mock_print.assert_called_with(
                "   Operation  Operand #1  Operand #2  Result\n"
                "37       Add           5           3       8\n"
                "38  Subtract          10           5       5"
            )

            # Ensure to_string was called as expected
            mock_to_string.assert_called_once()


def test_undo_empty_history():
    """Test undoing when history is empty."""
    # Reset the History singleton instance before each test
    History._instance = None

    history = History()

    with patch('builtins.open', MagicMock()), \
         patch.object(pd,
            'read_csv',
            return_value=pd.DataFrame(columns=["Operation", "Operand #1", "Operand #2", "Result"])
        ), \
         patch('builtins.print') as mock_print:
        # Try to undo when there are no operations in history
        history.undo_last()
        # Assert the correct message is printed
        mock_print.assert_called_with("No operations to undo.")


def test_print_empty_history():
    """Test printing history when history is empty without file writing."""
    # Reset the History singleton instance before each test
    History._instance = None

    # Create a new History instance for each test
    history = History()

    # Mock file-writing methods (open) to avoid file operations
    with patch('builtins.open', MagicMock()), \
         patch.object(pd,
            'read_csv',
            return_value=pd.DataFrame(columns=["Operation", "Operand #1", "Operand #2", "Result"])
        ), \
         patch('builtins.print') as mock_print:
        # Try to print history when it's empty
        history.print_history()
        # Assert the correct message is printed
        mock_print.assert_called_with("History is empty.")
