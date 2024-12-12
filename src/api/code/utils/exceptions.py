# api/utils/exceptions.py


# Lib
from datetime import datetime


"""
Define CustomException class to raise custom exceptions, inherit from Exception class (built-in Python class)
"""
class CustomException(Exception):
    def __init__(self, name : str, error_code: int, message: str = "", date: str = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))):
        self.name = name
        self.date = date
        self.error_code = error_code
        self.message = message