# api/unit_tests/utils_tests/common_functions_tests.py
# export PYTHONPATH=$(pwd)

# Suppress DeprecationWarnings from passlib and crypt (python 1.13)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module='passlib')
warnings.filterwarnings("ignore", category=DeprecationWarning, module='crypt')


# Lib
import jwt
import pytest
from unittest.mock import MagicMock, patch

from utils.common_functions import hash_string, get_current_user
from utils.config import PWD_CONTEXT, JWT_SECRET_KEY, ENCODING_ALGORITHM, PWD_CONTEXT
from utils.exceptions import CustomException



# TESTS
def test_hash_string_returns_string():
    input_string = "test_string"
    hashed_string = hash_string(input_string)
    assert isinstance(hashed_string, str), "The hashed output should be a string"

def test_hash_string_is_unique():
    input_string = "test_string"
    hashed_string1 = hash_string(input_string)
    hashed_string2 = hash_string(input_string)
    assert hashed_string1 != hashed_string2, "Hashes for the same input should be unique"

def test_hash_string_verification():
    input_string = "test_string"
    hashed_string = hash_string(input_string)
    assert PWD_CONTEXT.verify(input_string, hashed_string), "The hash should be verifiable with the original string"



@pytest.fixture
def valid_token():
    return jwt.encode({"username": "test_user"}, JWT_SECRET_KEY, algorithm=ENCODING_ALGORITHM)

@pytest.fixture
def invalid_token():
    return "invalid.token.here"

def test_get_current_user_success(valid_token):
    mock_oauth2_scheme = MagicMock(return_value=valid_token)
    with patch('services.auth.oauth2_scheme', mock_oauth2_scheme):
        decoded_token = get_current_user(token=valid_token)
        assert decoded_token["username"] == "test_user"

def test_get_current_user_invalid_token(invalid_token):
    mock_oauth2_scheme = MagicMock(return_value=invalid_token)
    with patch('services.auth.oauth2_scheme', mock_oauth2_scheme):
        with pytest.raises(CustomException) as excinfo:
            get_current_user(token=invalid_token)
        assert excinfo.value.name == 'Auth_token_error'
        assert excinfo.value.error_code == 500
        assert excinfo.value.message == "Invalid token"