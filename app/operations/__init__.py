'''
Operations:
    - Add
    - Subtract
    - Multiply
    - Divide
All inputs and outputs are typehinted to be floats.
'''

from abc import ABC, abstractmethod # Importing abstract base classes (ABC) and methods
import logging

class OperationTemplate(ABC):
    '''
    Abstract base class defining the template for arithmetic operations.
    All subclasses must implement the 'execute' method.

    
    Template method 'calculate' makes each operation:
        1. Validate input
        2. Execute the operation
        3. Logs the result
    '''
    def calculate(self, a: float, b: float) -> float:
        '''
        Template method for performing the operation:
            1. Validate input data
            2. Execute operation (each subclass provides its own implementation)
            3. Log the result of operation
        '''
        self.validate(a,b)
        result = self.execute(a,b)
        self.log_result(a, b, result)
        return result

    def validate(self, a: float, b: float):
        '''
        Checks if inputs are either integers or floats.
        Raises ValueError for invalid input.
        '''
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            logging.error("Invalid input: %s, %s (Inputs must be numbers)", a, b)
            raise ValueError("Both inputs must be numbers.")

    def log_result(self, a: float, b: float, result: float):
        '''Logs result of operation'''
        logging.info("Operation performed: %s and %s -> Result: %s", a, b, result)

    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        '''
        Abstract method ALL subclasses must implement.
        Each subclass has their own implementation.
        '''

    @abstractmethod
    def __repr__(self):
        '''
        Abstract method ALL subclasses must implement.
        Each subclass has their own implementation.
        '''

# --------------------------------
# ARITHMETIC OPERATIONS START HERE
# --------------------------------

class Add(OperationTemplate):
    '''
    Addition operation inheriting from OperationTemplate.
    '''
    def execute(self, a: float, b: float) -> float:
        '''
        Returns the sum of two floats.
        '''
        return a + b

    def __repr__(self):
        '''String representation for debugging'''
        return "Add"

class Subtract(OperationTemplate):
    '''
    Subtraction operation inheriting from OperationTemplate.
    '''
    def execute(self, a: float, b: float) -> float:
        '''
        Returns the difference of two floats.
        '''
        return a - b

    def __repr__(self):
        '''String representation for debugging'''
        return "Subtract"

class Multiply(OperationTemplate):
    '''
    Multiplication operation inheriting from OperationTemplate.
    '''
    def execute(self, a: float, b: float) -> float:
        '''
        Returns the product of two floats.
        '''
        return a * b

    def __repr__(self):
        '''String representation for debugging'''
        return "Multiply"

class Divide(OperationTemplate):
    '''
    Division operation inheriting from OperationTemplate.
    '''
    def execute(self, a: float, b: float) -> float:
        '''
        Returns the quotient of two floats.
        '''
        if b == 0:
            # Sends an error message when someone tries to divide by zero.
            logging.error("Attempted to divide by zero.")
            raise ValueError("Cannot divide by zero.")
        return a / b

    def __repr__(self):
        '''String representation for debugging'''
        return "Divide"
