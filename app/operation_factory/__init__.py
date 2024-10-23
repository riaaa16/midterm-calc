'''
Uses the Factory Pattern to dynamically instantiate the appropriate operation class
based on user input.

Exceptions:
- Raises KeyError if incorrect input is entered
'''

from app.operations import OperationTemplate, Add, Subtract, Multiply, Divide

class OperationFactory:
    '''
    Factory class that creates instances of operations based on the operation type.
    '''
    def create_operation(operation: str) -> OperationTemplate:
        '''
        Creates an instance of the correct operation subclass based on user input.
        '''

        # dictionary matching operation commands to operation class
        operations_map = {
            'add': Add(),
            'subtract': Subtract(),
            'multiply': Multiply(),
            'divide': Divide(),
        }

        try:
            operations_map[operation.lower()]
        except KeyError:
            raise KeyError("Operation does not exist.")
