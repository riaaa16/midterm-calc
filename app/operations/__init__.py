def Add(a, b):
    return a + b

def Subtract(a, b):
    return a - b

def Multiply(a, b):
    return a * b

def Divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a /b