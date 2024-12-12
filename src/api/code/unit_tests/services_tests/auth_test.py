# api/unit_tests/auth_test.py
# export PYTHONPATH=$(pwd)

# Suppress DeprecationWarnings from passlib and crypt (python 1.13)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module='passlib')
warnings.filterwarnings("ignore", category=DeprecationWarning, module='crypt')


# Lib
import jwt
import pytest
from unittest.mock import AsyncMock, patch

from utils.config import JWT_SECRET_KEY, ENCODING_ALGORITHM, PWD_CONTEXT
from utils.exceptions import CustomException
from utils.postgres_requests.user_requests import query_get_user_credentials_in_database



# Functions to test
from services.auth import encode_jwt, verify_password, verify_credentials




def test_encode_jwt():
    # Test data
    data = {"username": "test_user"}


    token = encode_jwt(**data)

    assert isinstance(token, str)
    assert len(token) > 0
    decoded_data = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ENCODING_ALGORITHM])
    assert decoded_data["username"] == "test_user"
    assert "exp" in decoded_data



def test_verify_password_success():
    # Test data
    given_password = "test_password"
    hashed_password = PWD_CONTEXT.hash(given_password)

    try:
        verify_password(given_password, hashed_password)
    except CustomException:
        pytest.fail("verify_password raised CustomException unexpectedly!")

def test_verify_password_failure():
    # Test data
    given_password = "test_password"
    hashed_password = PWD_CONTEXT.hash("different_password")

    with pytest.raises(CustomException) as excinfo:
        verify_password(given_password, hashed_password)
    assert excinfo.value.name == 'Auth_password_error'
    assert excinfo.value.error_code == 401
    assert excinfo.value.message == "Incorrect password"



@pytest.mark.asyncio
@patch('services.auth.get_postgres_client')
async def test_verify_credentials_success(mock_get_postgres_client):
    # Mock database response
    mock_client = AsyncMock()
    mock_client.fetchrow.return_value = {
        "username": "test_user",
        "password": PWD_CONTEXT.hash("test_password"),
        "verified": True
    }
    mock_get_postgres_client.return_value = mock_client

    # Test data
    given_username = "test_user"
    given_password = "test_password"

    # Call the function
    await verify_credentials(given_username, given_password)

    # Assertions
    mock_client.fetchrow.assert_called_once_with(query_get_user_credentials_in_database, given_username)
    mock_client.close.assert_called_once()

@pytest.mark.asyncio
@patch('services.auth.get_postgres_client')
async def test_verify_credentials_username_not_found(mock_get_postgres_client):
    # Mock database response
    mock_client = AsyncMock()
    mock_client.fetchrow.return_value = None
    mock_get_postgres_client.return_value = mock_client

    # Test data
    given_username = "non_existent_user"
    given_password = "test_password"

    # Call the function and assert exception
    with pytest.raises(CustomException) as excinfo:
        await verify_credentials(given_username, given_password)
    assert excinfo.value.name == 'Auth_username_error'
    assert excinfo.value.error_code == 401
    assert excinfo.value.message == "Username not found in the database"

    # Assertions
    mock_client.fetchrow.assert_called_once_with(query_get_user_credentials_in_database, given_username)

@pytest.mark.asyncio
@patch('services.auth.get_postgres_client')
async def test_verify_credentials_account_not_verified(mock_get_postgres_client):
    # Mock database response
    mock_client = AsyncMock()
    mock_client.fetchrow.return_value = {
        "username": "test_user",
        "password": PWD_CONTEXT.hash("test_password"),
        "verified": False
    }
    mock_get_postgres_client.return_value = mock_client

    # Test data
    given_username = "test_user"
    given_password = "test_password"

    # Call the function and assert exception
    with pytest.raises(CustomException) as excinfo:
        await verify_credentials(given_username, given_password)
    assert excinfo.value.name == 'Auth_verification_error'
    assert excinfo.value.error_code == 401
    assert excinfo.value.message == "Account not verified"

    # Assertions
    mock_client.fetchrow.assert_called_once_with(query_get_user_credentials_in_database, given_username)

@pytest.mark.asyncio
@patch('services.auth.get_postgres_client')
async def test_verify_credentials_incorrect_password(mock_get_postgres_client):
    # Mock database response
    mock_client = AsyncMock()
    mock_client.fetchrow.return_value = {
        "username": "test_user",
        "password": PWD_CONTEXT.hash("different_password"),
        "verified": True
    }
    mock_get_postgres_client.return_value = mock_client

    # Test data
    given_username = "test_user"
    given_password = "test_password"

    # Call the function and assert exception
    with pytest.raises(CustomException) as excinfo:
        await verify_credentials(given_username, given_password)
    assert excinfo.value.name == 'Auth_password_error'
    assert excinfo.value.error_code == 401
    assert excinfo.value.message == "Incorrect password"

    # Assertions
    mock_client.fetchrow.assert_called_once_with(query_get_user_credentials_in_database, given_username)