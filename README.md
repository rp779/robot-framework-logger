# Robot Framework with Custom Logger

This example shows how to integrate your custom Python logger with Robot Framework tests.

## Files

- `robot_logger.py` - Your custom logger (80 lines)
- `test_suite.robot` - Example Robot Framework test suite
- `keywords.resource` - Reusable Robot Framework keywords
- `run_tests.py` - Script to run the tests
- `requirements.txt` - Dependencies

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the tests:**
   ```bash
   python run_tests.py
   ```
   
   Or directly with Robot Framework:
   ```bash
   robot test_suite.robot
   ```

## How It Works

### 1. Custom Logger (`robot_logger.py`)
Your simple Python logger with color support that Robot Framework can use directly:
```python
from robot_logger import RobotLogger
logger = RobotLogger()
logger.start_test("My Test")
logger.step("Do something")
logger.pass_test("Success!")
```

### 2. Robot Framework Integration
Robot Framework can directly use your Python logger as a library:
```robot
*** Settings ***
Library    robot_logger.py

*** Test Cases ***
My Test
    Start Test    My Test
    Step          Do something
    Pass Test     Success!
    End Test      PASS
```

### 3. Test Suite (`test_suite.robot`)
Example Robot Framework tests that use your logger:
- User Login Test
- Form Validation Test  
- API Endpoint Test
- Failed Test Example

### 4. Keywords (`keywords.resource`)
Reusable keywords that integrate with your logger:
- Page navigation keywords
- Form interaction keywords
- API testing keywords

## Key Features

✅ **Color-coded output** in terminal
✅ **Test context tracking** with step numbers
✅ **Rich formatting** with timestamps and icons
✅ **Integration** with Robot Framework keywords
✅ **Reusable** across multiple test suites
✅ **Simple** - just 4 files total

## Example Output

When you run the tests, you'll see:
```
────────────────────────────────────────
🚀 User Login Test
────────────────────────────────────────
23:45:12 [INFO] | User Login Test | Step 1: Navigate to login page
23:45:15 [PASS] | User Login Test | Successfully navigated to login page
23:45:15 [INFO] | User Login Test | Step 2: Enter username
23:45:16 [PASS] | User Login Test | Username entered successfully
...
────────────────────────────────────────
✅ User Login Test: PASS
────────────────────────────────────────
```

## Customization

You can easily extend the logger by:
1. Adding new methods to `robot_logger.py`
2. Creating corresponding keywords in `CustomLogger.py`
3. Using them in your Robot Framework tests

This gives you the best of both worlds - simple Python logging with full Robot Framework integration!
