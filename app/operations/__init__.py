'''
Can add, subtract, multiply, and divide. All inputs and outputs
are typehinted to be floats.
'''

def add(a: float, b: float) -> float:
    '''
    Returns the sum of two floats.
    '''
    return a + b

def subtract(a: float, b: float) -> float:
    '''
    Returns the difference of two floats.
    '''
    return a - b

def multiply(a: float, b: float) -> float:
    '''
    Returns the product of two floats.
    '''
    return a * b

def divide(a: float, b: float) -> float:
    '''
    Returns the quotient of two floats.
    '''
    if b == 0:
        # Sends an error message when someone tries to divide by zero.
        raise ValueError("Cannot divide by zero.")
    return a /b
