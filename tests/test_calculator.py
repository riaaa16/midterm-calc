"""
Unit tests for the calculator REPL.

This module tests the calculator's arithmetic operations and error handling 
for invalid inputs, utilizing the `unittest` framework and `unittest.mock` 
for input simulation and output capture.
"""

import unittest
from unittest.mock import patch, MagicMock
from app.calculator import calculator

class TestCalculator(unittest.TestCase):
    """
    Test cases for the calculator REPL.
    """

    @patch('builtins.input', side_effect=[
        'add 1 2',   # Test addition
        'subtract 5 3',  # Test subtraction
        'multiply 3 4',  # Test multiplication
        'divide 8 2',    # Test division
        'exit'           # Exit command
    ])
    @patch('app.operation_factory.OperationFactory.create_operation')
    def test_calculator_operations(self, mock_create_operation, _mock_input):
        """
        Test various arithmetic operations performed in the calculator.
        """
        # Setup mock operations
        mock_add = MagicMock()
        mock_subtract = MagicMock()
        mock_multiply = MagicMock()
        mock_divide = MagicMock()

        mock_create_operation.side_effect = [
            mock_add, mock_subtract, mock_multiply, mock_divide
        ]

        # Mock return values for calculations
        mock_add.calculate.return_value = 3
        mock_subtract.calculate.return_value = 2
        mock_multiply.calculate.return_value = 12
        mock_divide.calculate.return_value = 4

        with patch('builtins.print') as mock_print:
            calculator()

            # Check that the operations were called correctly
            mock_add.calculate.assert_called_once_with(1.0, 2.0)
            mock_subtract.calculate.assert_called_once_with(5.0, 3.0)
            mock_multiply.calculate.assert_called_once_with(3.0, 4.0)
            mock_divide.calculate.assert_called_once_with(8.0, 2.0)

            # Check output for each operation
            mock_print.assert_any_call("Result: 3")
            mock_print.assert_any_call("Result: 2")
            mock_print.assert_any_call("Result: 12")
            mock_print.assert_any_call("Result: 4")
            mock_print.assert_any_call("Exiting calculator...")

    @patch('builtins.input', side_effect=[
        'invalid input',
        'exit'
    ])
    @patch('builtins.print')
    def test_invalid_input(self, mock_print, _mock_input):
        """
        Test handling of invalid input.
        """
        calculator()

        # Check that the invalid input message was printed
        mock_print.assert_any_call(
            "Invalid input. Please enter a valid operation and two numbers. "
            "Type 'help' for instructions."
        )

    @patch('builtins.input', side_effect=[
        'add abc 2', 
        'subtract 5 3.0', 
        'multiply 3 four', 
        'divide 8 0',
        'exit'
    ])
    @patch('builtins.print')
    def test_various_invalid_inputs(self, mock_print, _mock_input):
        """
        Test handling of various invalid inputs.
        """
        calculator()

        expected_calls = [
            "Invalid input. Please enter a valid operation and two numbers. "
            "Type 'help' for instructions.",
            "Invalid input. Please enter a valid operation and two numbers. "
            "Type 'help' for instructions.",
            "Invalid input. Please enter a valid operation and two numbers. "
            "Type 'help' for instructions.",
            "Invalid input. Please enter a valid operation and two numbers. "
            "Type 'help' for instructions."
        ]

        # Check that the invalid input message is printed for each invalid input
        for expected_call in expected_calls:
            mock_print.assert_any_call(expected_call)

    @patch('builtins.input', side_effect=[
        'help',  # Test help command
        'exit'   # Exit command
    ])
    @patch('builtins.print')
    def test_help_command(self, mock_print, _mock_input):
        """
        Test the help command in the calculator.
        """
        calculator()

        # Expected printed output for help command
        expected_calls = [
            "Available commands:",
            "    ✶ add      <num1> <num2>    : Adds two numbers.",
            "    ✶ subtract <num1> <num2>    : Subtracts two numbers.",
            "    ✶ multiply <num1> <num2>    : Multiplies two numbers.",
            "    ✶ divide   <num1> <num2>    : Divides two numbers.",
            "    ✶ exit                      : Exits the calculator."
        ]

        # Check that each expected output was printed
        for expected_call in expected_calls:
            mock_print.assert_any_call(expected_call)

if __name__ == '__main__':
    unittest.main()
