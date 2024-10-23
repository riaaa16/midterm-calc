'''
Testing operation factory with parameterized tests
'''

import pytest
from app.operation_factory import OperationFactory
from app.operations import Add, Subtract, Multiply, Divide

@pytest.mark.parametrize("operation_name, expected_class", [
    ('add', Add),
    ('subtract', Subtract),
    ('multiply', Multiply),
    ('divide', Divide),
])
def test_create_operations(operation_name, expected_class):
    """Test creating operations using parameterized tests."""
    operation = OperationFactory.create_operation(operation_name)
    assert isinstance(operation, expected_class), (
        f"Expected an instance of {expected_class.__name__}."
    )

def test_create_invalid_operation():
    """Test creating an invalid operation."""
    with pytest.raises(ValueError, match="Operation does not exist."):
        OperationFactory.create_operation('invalid_operation')

def test_create_case_insensitive_operation():
    """Test creating operations with different cases."""
    operation = OperationFactory.create_operation('ADd')
    assert isinstance(operation, Add), "Expected an instance of Add."
