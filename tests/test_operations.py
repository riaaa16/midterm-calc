import pytest
from app.operations import Add, Subtract, Multiply, Divide

def test_addition():
    assert Add(1,2) == 3

def test_subtraction():
    assert Subtract(3,2) == 1

def test_multiplication():
    assert Multiply(2,5) == 10

def test_division():
    assert Divide(10,2) == 5

def test_division_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        Divide(10,0)