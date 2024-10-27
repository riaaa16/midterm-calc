'''
Can add, subtract, multiply, and divide. All inputs and outputs
are typehinted to be floats.
'''

from abc import ABC, abstractmethod # Creating abstract base classes (ABC)
import logging

class OperationTemplate(ABC):
    '''
    Abstract base class that creates a template the inherting operation subclasses
    should follow.

    Before each operation is executed, the inputs are validated.
    '''
    def calculate(self, a: float, b: float) -> float:
        '''
        For each subclass inheriting from Operation Template:
            1. Validate input
            2. Execute operation
        '''
        self.validate(a,b)
        result = self.execute(a,b)
        self.log_result(a, b, result)
        return result

    def validate(self, a: float, b: float):
        '''
        Checks inputs are numbers before calculating
        '''
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            logging.error("Invalid input: %s, %s (Inputs must be numbers)", a, b)
            raise ValueError("Both inputs must be numbers.")
        
    def log_result(self, a: float, b: float, result: float):
        '''Logs result of calculation'''
        logging.info(f"Operation performed: {a} and {b} -> Result: {result}")

    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        '''
        Abstract methods ALL subclasses must implement.
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

class Subtract(OperationTemplate):
    '''
    Subtraction operation inheriting from OperationTemplate.
    '''
    def execute(self, a: float, b: float) -> float:
        '''
        Returns the difference of two floats.
        '''
        return a - b

class Multiply(OperationTemplate):
    '''
    Multiplication operation inheriting from OperationTemplate.
    '''
    def execute(self, a: float, b: float) -> float:
        '''
        Returns the product of two floats.
        '''
        return a * b

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
    
# -------------------------------
# ARITHMETIC OPERATIONS END HERE
# -------------------------------
