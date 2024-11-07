'''
Uses OperationTemplate class provided by Operation_Factory to perform operations.
'''
from dataclasses import dataclass
from app.operations import OperationTemplate

@dataclass
class Calculation:
    '''
    Runs calculate method on operands.
    Decorator automatically generates __init__ methods.
    '''
    operation: OperationTemplate  # operation to perform (add, subtract, etc.)
    operand1: float  # first operand
    operand2: float  # second operand

    def __repr__(self) -> str:
        '''String representation for debugging & logging'''
        return (
            f"Calculation({self.operation}, {self.operand1}, {self.operand2})"
        )

    def __str__(self) -> str:
        '''String representation for users'''
        result = self.operation.calculate(self.operand1, self.operand2)  # Perform the calculation
        return (
            f"{self.operand1} {self.operation} {self.operand2} = {result}"
        )

    def perform_operation(self):
        '''Performs operation with provided operands, delegates to operation'''
        result = self.operation.calculate(self.operand1, self.operand2)  # Perform the calculation
        return result  # return result
