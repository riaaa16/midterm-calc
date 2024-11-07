'''
User can interact with this calculator in the terminal to perform basic
arithmetic operations: addition, subtraction, multiplication, and division.
'''

import logging
import logging.config
import os
from dotenv import load_dotenv
from app.operation_factory import OperationFactory
from app.calculation import Calculation
from app.history_manager import History

def calculator():
    '''
    Calculator REPL that loops continuously to take user input.
    Raises exceptions for invalid input.
    Will end once the user types 'exit'.
    '''

    load_dotenv()

    if os.getenv('TEST_MODE') != 'True':
         # Configure logger if TEST_MODE is FALSE
        logging.config.fileConfig('logging.conf')

    logging.getLogger('sampleLogger')

    # Flag to track calculator's start
    start = False

    history = History() # Create history instance

    print("Welcome to the calculator! Type 'help' for a list of commands.")

    # Start REPL
    while True:
        if not start:
            logging.info("Calculator started.")
            start = True # After calculator starts, set start to True

        user_input = input("Enter an command: ")
        command = user_input.lower()

        if command == 'help':
            print("Available commands:")
            print("    ✶ add      <num1> <num2>    : Adds two numbers.")
            print("    ✶ subtract <num1> <num2>    : Subtracts two numbers.")
            print("    ✶ multiply <num1> <num2>    : Multiplies two numbers.")
            print("    ✶ divide   <num1> <num2>    : Divides two numbers.")
            print("    ✶ list                      : Shows operation history.")
            print("    ✶ undo                      : Removes last operation from history.")
            print("    ✶ exit                      : Exits the calculator.")
            continue

        # Exit REPL
        if command == 'exit':
            logging.info("Calculator exited.")
            print("Exiting calculator...")
            break

        # Undo last comment
        if command == 'undo':
            history.undo_last()
            continue

        # Print operations performed in this instance's session
        if command == 'list':
            history.print_history()
            continue

        try:
            # LBYL - checking user input is correct before trying operations
            # Split user input into 3 components
            operation_str, num1_str, num2_str = user_input.split()

            # converting operation_str to lowercase
            operation_str = operation_str.lower()

            # Convert operands into floats
            num1, num2 = float(num1_str), float(num2_str)

            # Creat appropriate operation insance based on user input
            operation = OperationFactory.create_operation(operation_str)

            # Perform operation
            calculation  = Calculation(operation, num1, num2)
            result = calculation.perform_operation()

            # Print result
            print(f"Result: {result}")

            # Add calculation to history
            history.add_to_history(operation, num1, num2, result)

        except ValueError as e:
            logging.error("Invalid input or error: %s", e)
            print(
                "Invalid input. Please enter a valid operation and two numbers. "
                "Type 'help' for instructions."
            )
