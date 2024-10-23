'''
User can interact with this calculator in the terminal to perform basic
arithmetic operations: addition, subtraction, multiplication, and division.
'''

from app.operation_factory import OperationFactory

def calculator():
    '''
    Calculator REPL that loops continuously to take user input.
    Raises exceptions for invalid input.
    Will end once the user types 'exit'.
    '''
    print("Welcome to the calculator! Type 'help' for a list of commands.")

    # Start REPL
    while True:
        user_input = input("Enter an command: ")

        if user_input.lower() == 'help':
            print("Available commands:")
            print("    ✶ add      <num1> <num2>    : Adds two numbers.")
            print("    ✶ subtract <num1> <num2>    : Subtracts two numbers.")
            print("    ✶ multiply <num1> <num2>    : Multiplies two numbers.")
            print("    ✶ divide   <num1> <num2>    : Divides two numbers.")
            print("    ✶ exit                      : Exits the calculator.")

        # Exit REPL
        if user_input.lower() == 'exit':
            print("Exiting calculator...")
            break

        try:
            # LBYL - checking user input is correct before trying operations
            # Split user input into 3 components
            operation_str, num1_str, num2_str = user_input.split()

            # Convert operands into floats
            num1, num2 = float(num1_str), float(num2_str)

            # Matching operation string to correct operation class
            operation = OperationFactory.create_operation(operation_str)

            result = operation.calculate(num1, num2)
            print(f"Result: {result}")

        except ValueError:
            print(
                "Invalid input. Please enter a valid operation and two numbers. "
                "Type 'help' for instructions."
            )
