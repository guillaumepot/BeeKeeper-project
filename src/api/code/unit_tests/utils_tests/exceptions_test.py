# api/unit_tests/utils_tests/exceptions_test.py
# export PYTHONPATH=$(pwd)

# Suppress DeprecationWarnings from passlib and crypt (python 1.13)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module='passlib')
warnings.filterwarnings("ignore", category=DeprecationWarning, module='crypt')



# Lib
from datetime import datetime, timedelta
import pytest


from utils.exceptions import CustomException



def test_custom_exception_initialization():
    # Test data
    name = "TestError"
    error_code = 400
    message = "This is a test error"
    date = "2023-01-01 00:00:00"

    # Create an instance of CustomException
    exception = CustomException(name, error_code, message, date)

    # Asserts
    assert exception.name == name
    assert exception.error_code == error_code
    assert exception.message == message
    assert exception.date == date

def test_custom_exception_default_date():
    # Test data
    name = "TestError"
    error_code = 400
    message = "This is a test error"

    # Create an instance of CustomException without providing date
    exception = CustomException(name, error_code, message)

    # Asserts
    assert exception.name == name
    assert exception.error_code == error_code
    assert exception.message == message

    # Check if the date is set to the current date within a small range
    now = datetime.now()
    exception_date = datetime.strptime(exception.date, "%Y-%m-%d %H:%M:%S")
    assert now - timedelta(seconds=10) <= exception_date <= now + timedelta(seconds=10)