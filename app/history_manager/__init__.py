"""
Creates a Singleton history instance and saves history to a table using pandas.

Features:
- Loads history from an existing CSV or creates one if it doesn't exist.
- Records Operation, Operands, and Result in CSV file.
- Undoes the last operation.
- Prints history for ONLY that session.
- Closes the history file once done.
"""

import logging
import os
import csv
import pandas as pd
from dotenv import load_dotenv
from app.operations import OperationTemplate

class History:
    """Singleton class to manage and record a history of operations in a CSV file."""

    _instance = None

    def __new__(cls):
        """Create or return the singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the history."""
        if not hasattr(self, '_initialized'):  # Check if initialization has occurred
            load_dotenv()
            self.filename = os.getenv('HISTORY_FILENAME', 'history.csv')
            self._create_csv_writer()

            self.counter = 0  # Counter for number of operations
            self._initialized = True  # Mark as initialized

    def _create_csv_writer(self):
        """Create or open the CSV file for appending history."""
        if not os.path.exists(self.filename):
            # If file doesn't exist, create it and write the header
            with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Operation', 'Operand #1', 'Operand #2', 'Result'])
                logging.info("History file created.")
        else:
            logging.info("History file loaded.")

    def add_to_history(self, operation: OperationTemplate, operand1: float, operand2: float, result: float):
        """Add an operation to the history."""
        operation_name = operation.__class__.__name__

        # Open the file to append data to it
        with open(self.filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([operation_name, operand1, operand2, result])
            file.flush()
            logging.info("Added '%s %s %s = %s' to history.", operand1, operation_name, operand2, result)

        # Increment the operation counter
        self.counter += 1

    def undo_last(self):
        """Undo the last operation in the history."""
        df = pd.read_csv(self.filename)  # Load file into a DataFrame

        if self.counter == 0:
            print("No operations to undo.")
            return

        # Getting the last row and unpacking it into variables
        last_row = df.iloc[-1]
        operation, operand1, operand2, result = last_row

        # Remove the last row
        df = df.drop(index=df.index[-1])

        print("Removed operation")
        print(f"    {operand1} {operation} {operand2} = {result}")
        print("from history.")

        # Save the modified history back to the file
        df.to_csv(self.filename, index=False)

        # Decrement the operation counter
        self.counter -= 1

        logging.info("Removed")
        logging.info("    %s %s %s = %s", operand1, operation, operand2, result)
        logging.info("from history.")

    def print_history(self):
        """Print only that session's history."""
        if self.counter == 0:
            print("History is empty.")
            return

        df = pd.read_csv(self.filename)  # Load CSV file
        print(df.tail(self.counter).to_string())  # Print only the instance's history
