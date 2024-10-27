from app.operations import OperationTemplate

class Calculation:
    def perform_operation(self, operation: OperationTemplate, operand1: float, operand2: float):
        result = operation.calculate(operand1, operand2)  # Perform the calculation
        return result
