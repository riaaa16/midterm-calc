# Midterm Calculator

## Video Demonstration
You can watch a brief video demonstration [HERE](https://youtu.be/z1LdCteCxDQ?si=hGELXMh-ZD_0t6B).

## Installation & Configuration
1. Install all of the packages with `pip install -r requirements.txt`
2. Create an .env file in your root directory that resembles the example below.
```python
FILENAME=history.csv
# Configure to True to shut off logs in app.calculator
TEST_MODE=False
```
3. Create a `logging.conf` file in your root directory that resembles the example below.
```python
[loggers]
keys=root,sampleLogger

[handlers]
keys=fileHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=DEBUG
handlers=fileHandler

[logger_sampleLogger]
level=DEBUG
handlers=fileHandler
qualname=sampleLogger
propagate=0

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=simpleFormatter
args=('calculator.log',)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=%Y-%m-%d %H:%M:%S

```
5. Enter  `python main.py` in your terminal to run the calculator program.

## Design Patterns
### Template Method Pattern
Used in the `OperationTemplate` to define a framework for subclasses. The `calculate` method defines the structure of operations.
All subclasses operate in this order:
1. Validate input
2. Execute Operation
3. Log result

Subclasses implement their own `execute` method in order to perform the specific operation.

Full code can be found [HERE](https://github.com/riaaa16/midterm-calc/blob/main/app/operations/__init__.py#L24)
```python
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

    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        '''
        Abstract method ALL subclasses must implement.
        Each subclass has their own implementation.
        '''
```
### Factory Pattern & Strategy Pattern
Used in `OperationFactory` to instantiate the appropriate operation class (`Add`, `Subtract`, `Multiply`, `Divide`) based on user input.
The class doesn't have to be specified in the parameters, and is instantiated at runtime.

Full code can be found [HERE](https://github.com/riaaa16/midterm-calc/blob/main/app/operation_factory/__init__.py#L17)
```python
class OperationFactory:
    @staticmethod
    def create_operation(operation: str) -> OperationTemplate:
        '''Creates an instance of the correct operation subclass based on user input.'''

        # Dictionary matching operation commands to operation class
        operations_map = {
            'add': Add(),
            'subtract': Subtract(),
            'multiply': Multiply(),
            'divide': Divide(),
        }

        try:
            return operations_map[operation.lower()]
        except KeyError as exc:
            raise ValueError("Operation does not exist.") from exc
```

The Strategy Pattern is implemented in the `calculator`.

Full code can be found [HERE](https://github.com/riaaa16/midterm-calc/blob/ada4e3ce2a9b435b5630248d4ae3173c69803db2/app/calculator/__init__.py#L84)
```python
try:
            # LBYL - checking user input is correct before trying operations
            # Split user input into 3 components
            operation_str, num1_str, num2_str = user_input.split()

            # converting operation_str to lowercase
            operation_str = operation_str.lower()

            # Convert operands into floats
            num1, num2 = float(num1_str), float(num2_str)

            # Creat appropriate operation insance based on user input
            operation = OperationFactory.create_operation(operation_str)

            # Perform operation
            calculation  = Calculation(operation, num1, num2)
            result = calculation.perform_operation()

            # Print result
            print(f"Result: {result}")
```
### Singleton Pattern
Used in `History` to ensure there is only one instance. The `__new__` method checks if an instance exists before instantiating.

Full code can be found [HERE](https://github.com/riaaa16/midterm-calc/blob/main/app/history_manager/__init__.py#L23)
```python
class History:
    """Singleton class to manage and record a history of operations in a CSV file."""

    _instance = None

    def __new__(cls):
        """Create or return the singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```
### Facade Pattern
The `History` class uses Pandas and file I/O in order to load, save, add, undo, and list operations. It handles file creation, the .csv set up, and the adding of operations to the history for the user. The user can only interact with the history through `undo_last()` and `print_history()`.

Full code can be found [HERE](https://github.com/riaaa16/midterm-calc/blob/main/app/history_manager/__init__.py#L18)
```python
class History:
    """Singleton class to manage and record a history of operations in a CSV file."""

    _instance = None

    def __new__(cls):
        """Create or return the singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the history."""
        if not hasattr(self, '_initialized'):  # Check if initialization has occurred
            load_dotenv()
            self.filename = os.getenv('HISTORY_FILENAME', 'history.csv')
            self._create_csv_writer()

            self.counter = 0  # Counter for number of operations
            self._initialized = True  # Mark as initialized

    def _create_csv_writer(self):
        """Create or open the CSV file for appending history."""
        if not os.path.exists(self.filename):
            # If file doesn't exist, create it and write the header
            with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Operation', 'Operand #1', 'Operand #2', 'Result'])
                logging.info("History file created.")
        else:
            logging.info("History file loaded.")

    def add_to_history(self, operation: OperationTemplate, operand1: float, operand2: float, result: float):
        """Add an operation to the history."""

        # Open the file to append data to it
        with open(self.filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([operation, operand1, operand2, result])
            file.flush()
            logging.info("Added '%s %s %s = %s' to history.", operand1, operation, operand2, result)

        # Increment the operation counter
        self.counter += 1

    def undo_last(self):
        """Undo the last operation in the history."""
        df = pd.read_csv(self.filename)  # Load file into a DataFrame

        if self.counter == 0:
            print("No operations to undo.")
            return

        # Getting the last row and unpacking it into variables
        last_row = df.iloc[-1]
        operation, operand1, operand2, result = last_row

        # Remove the last row
        df = df.drop(index=df.index[-1])

        print("Removed operation")
        print(f"    {operand1} {operation} {operand2} = {result}")
        print("from history.")

        # Save the modified history back to the file
        df.to_csv(self.filename, index=False)

        # Decrement the operation counter
        self.counter -= 1

        logging.info("Removed")
        logging.info("    %s %s %s = %s", operand1, operation, operand2, result)
        logging.info("from history.")

    def print_history(self):
        """Print only that session's history."""
        if self.counter == 0:
            print("History is empty.")
            return

        df = pd.read_csv(self.filename)  # Load CSV file
        print(df.tail(self.counter).to_string())  # Print only the instance's history
```
## Logging
Once you set up your `logging.conf`, you will be able to track the Calculator's log history in a .log file. Logging is implemented in multiple modules in order to track what operations are being created and to catch exceptions. The following are some examples showcasing how logging is used throughout the code.

In `OperationTemplate`, each subclass logs its parameters and result through the `log_result` method.
```python
    def log_result(self, a: float, b: float, result: float):
        '''Logs result of operation'''
        logging.info("Operation performed: %s and %s -> Result: %s", a, b, result)
```

The `OperationFactory` uses logging to track what operation is being instantiated and to catch errors.
```python
        try:
            logging.debug("Creating operation: %s", operation)
            # Returns corresponding operation
            return operations_map[operation.lower()]
        except KeyError as exc:
            # Raise value error if operation is not recognized
            logging.error("Tried to call unknown operation.")
            raise ValueError("Operation does not exist.") from exc

```

When adding operations to the an instance of `History`, the `add_to_history` method logs the operation, operands, and result being performed.

```python
    def add_to_history(self, operation: OperationTemplate, operand1: float, operand2: float, result: float):
        """Add an operation to the history."""

        # Open the file to append data to it
        with open(self.filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([operation, operand1, operand2, result])
            file.flush()
            logging.info("Added '%s %s %s = %s' to history.", operand1, operation, operand2, result)

        # Increment the operation counter
        self.counter += 1
```

### Example `.log`
This is an example of what the logs for one Calculator session may look like.
```logtalk
2024-11-06 22:18:48 - root - INFO - Calculator exited.
2024-11-06 23:15:00 - root - INFO - History file loaded.
2024-11-06 23:15:00 - root - INFO - Calculator started.
2024-11-06 23:15:03 - root - DEBUG - Creating operation: add
2024-11-06 23:15:03 - root - INFO - Operation performed: 1.0 and 2.0 -> Result: 3.0
2024-11-06 23:15:03 - root - INFO - Added '1.0 Add 2.0 = 3.0' to history.
2024-11-06 23:15:08 - root - DEBUG - Creating operation: divide
2024-11-06 23:15:08 - root - INFO - Operation performed: 3.0 and 4.0 -> Result: 0.75
2024-11-06 23:15:08 - root - INFO - Added '3.0 Divide 4.0 = 0.75' to history.
2024-11-06 23:15:10 - root - DEBUG - Creating operation: divide
2024-11-06 23:15:10 - root - ERROR - Attempted to divide by zero.
2024-11-06 23:15:10 - root - ERROR - Invalid input or error: Cannot divide by zero.
2024-11-06 23:15:18 - root - DEBUG - Creating operation: multiply
2024-11-06 23:15:18 - root - INFO - Operation performed: 1.0 and 0.0 -> Result: 0.0
2024-11-06 23:15:18 - root - INFO - Added '1.0 Multiply 0.0 = 0.0' to history.
2024-11-06 23:15:20 - root - INFO - Removed
2024-11-06 23:15:20 - root - INFO -     1.0 Multiply 0.0 = 0.0
2024-11-06 23:15:20 - root - INFO - from history.
2024-11-06 23:15:27 - root - DEBUG - Creating operation: subtract
2024-11-06 23:15:27 - root - INFO - Operation performed: 2.0 and 1.0 -> Result: 1.0
2024-11-06 23:15:27 - root - INFO - Added '2.0 Subtract 1.0 = 1.0' to history.
2024-11-06 23:15:29 - root - INFO - Calculator exited.
```
## Environment Variables
An `.env` variable is used in `History` to determine where the calculation history should be written.

Full code can be found [HERE](https://github.com/riaaa16/midterm-calc/blob/ada4e3ce2a9b435b5630248d4ae3173c69803db2/app/history_manager/__init__.py#L29)
```python
    def __init__(self):
        """Initialize the history."""
        if not hasattr(self, '_initialized'):  # Check if initialization has occurred
            load_dotenv()
            self.filename = os.getenv('HISTORY_FILENAME', 'history.csv')
            self._create_csv_writer()

            self.counter = 0  # Counter for number of operations
            self._initialized = True  # Mark as initialized

    def _create_csv_writer(self):
        """Create or open the CSV file for appending history."""
        if not os.path.exists(self.filename):
            # If file doesn't exist, create it and write the header
            with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Operation', 'Operand #1', 'Operand #2', 'Result'])
                logging.info("History file created.")
        else:
            logging.info("History file loaded.")
```

An `.env` variable is used in `calculator` to set the testing environment. The test file `test_calculator.py` writes actual logs after performing operations. In order to prevent this from happening, the logger is configured based on whether or not `TEST_MODEE` is `True` or `False`. The `.env` variable is mocked in `test_calculator.py` to be `True`, but it can be configured in the `.env` as `False` if you wish to prevent logs from being written when running `python main.py`.

### In the Calculator
Full code can be found [HERE](https://github.com/riaaa16/midterm-calc/blob/ada4e3ce2a9b435b5630248d4ae3173c69803db2/app/calculator/__init__.py#L23)
```python
def calculator():
    '''
    Calculator REPL that loops continuously to take user input.
    Raises exceptions for invalid input.
    Will end once the user types 'exit'.
    '''

    load_dotenv()

    if os.getenv('TEST_MODE') != 'True':
         # Configure logger if TEST_MODE is FALSE
        logging.config.fileConfig('logging.conf')

    logging.getLogger('sampleLogger')
```

### In the Calculator Test File
Full code can be found [HERE](https://github.com/riaaa16/midterm-calc/blob/ada4e3ce2a9b435b5630248d4ae3173c69803db2/tests/test_calculator.py#L19)
```python
@pytest.fixture(autouse=True)
def set_test_mode(monkeypatch):
    """Fixture to set TEST_MODE to 'True' during tests."""
    monkeypatch.setenv("TEST_MODE", "True")
    yield
    # After the test, TEST_MODE will be reset to its original value automatically
```
## Try/catch & Exceptions
Try/catch statements are used in the `calculator` to check the user input before performing the operation. This is an example of LBYL (Look Before You Leap). EAFP (Easier to Ask for Forgiveness than Permission) is implemented in exception statements. Incorrect user input is handled after it is passed.

Full code can be found [HERE](https://github.com/riaaa16/midterm-calc/blob/ada4e3ce2a9b435b5630248d4ae3173c69803db2/app/calculator/__init__.py#L72C9-L101C14)
```python
try:
            # LBYL - checking user input is correct before trying operations
            # Split user input into 3 components
            operation_str, num1_str, num2_str = user_input.split()

            # converting operation_str to lowercase
            operation_str = operation_str.lower()

            # Convert operands into floats
            num1, num2 = float(num1_str), float(num2_str)

            # Creat appropriate operation insance based on user input
            operation = OperationFactory.create_operation(operation_str)

            # Perform operation
            calculation  = Calculation(operation, num1, num2)
            result = calculation.perform_operation()

            # Print result
            print(f"Result: {result}")

            # Add calculation to history
            history.add_to_history(operation, num1, num2, result)

        except ValueError as e:
            logging.error("Invalid input or error: %s", e)
            print(
                "Invalid input. Please enter a valid operation and two numbers. "
                "Type 'help' for instructions."
            )
```

The `OperationFactory` also uses try/catch statements to catch key errors. If a user tries to enter an operation that is spelled incorrectly or isn't listed, then it will return a `KeyError`. This is another example of LBYL.

Full code can be found [HERE](https://github.com/riaaa16/midterm-calc/blob/ada4e3ce2a9b435b5630248d4ae3173c69803db2/app/operation_factory/__init__.py#L30)
```python
        try:
            logging.debug("Creating operation: %s", operation)
            return operations_map[operation.lower()]
        except KeyError as exc:
            logging.error("Tried to call unknown operation.")
            raise ValueError("Operation does not exist.") from exc
```
