# api/unit_tests/postgres_connectors_test.py
# export PYTHONPATH=$(pwd)

# Suppress DeprecationWarnings from passlib and crypt (python 1.13)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module='passlib')
warnings.filterwarnings("ignore", category=DeprecationWarning, module='crypt')


# Lib
import asyncpg
import pytest
from unittest.mock import patch, AsyncMock

from models.users_base_models import Password
from utils.exceptions import CustomException
from utils.postgres_requests.user_requests import query_get_user_secure_data, query_get_user_info_data, query_get_username, query_force_user_verified_true, query_update_user_last_login



# Functions to test
from services.postgres_connectors import get_postgres_client, get_user_data_from_database, get_user_info_data, query_update_user_info_data, update_user_info_data, check_if_user_exists_in_database, force_verified_user_to_true, update_user_password, update_user_last_login



@pytest.mark.asyncio
async def test_get_postgres_client_timeout():
    with patch('asyncpg.connect', new_callable=AsyncMock) as mock_connect:
        mock_connect.side_effect = asyncpg.exceptions.ConnectionDoesNotExistError("Timeout error")
        with pytest.raises(CustomException) as exc_info:
            await get_postgres_client("test_db")
        assert exc_info.value.name == 'Error: Postgres connection'
        assert exc_info.value.error_code == 500
        assert "Timeout error" in exc_info.value.message


@pytest.mark.asyncio
async def test_get_postgres_client_bad_credentials():
    with patch('asyncpg.connect', new_callable=AsyncMock) as mock_connect:
        mock_connect.side_effect = asyncpg.exceptions.InvalidPasswordError("Invalid credentials")
        with pytest.raises(CustomException) as exc_info:
            await get_postgres_client("test_db")
        assert exc_info.value.name == 'Error: Postgres connection'
        assert exc_info.value.error_code == 500
        assert "Invalid credentials" in exc_info.value.message


@pytest.mark.asyncio
async def test_get_postgres_client_bad_database_name():
    with patch('asyncpg.connect', new_callable=AsyncMock) as mock_connect:
        mock_connect.side_effect = asyncpg.exceptions.InvalidCatalogNameError("Invalid database name")
        with pytest.raises(CustomException) as exc_info:
            await get_postgres_client("invalid_db")
        assert exc_info.value.name == 'Error: Postgres connection'
        assert exc_info.value.error_code == 500
        assert "Invalid database name" in exc_info.value.message


@pytest.mark.asyncio
async def test_get_postgres_client_success():
    with patch('asyncpg.connect', new_callable=AsyncMock) as mock_connect:
        mock_client = AsyncMock()
        mock_connect.return_value = mock_client
        client = await get_postgres_client("test_db")
        assert client == mock_client


@pytest.mark.asyncio
async def test_get_postgres_client_network_issue():
    with patch('asyncpg.connect', new_callable=AsyncMock) as mock_connect:
        mock_connect.side_effect = OSError("Network issue")
        with pytest.raises(CustomException) as exc_info:
            await get_postgres_client("test_db")
        assert exc_info.value.name == 'Error: Postgres connection'
        assert exc_info.value.error_code == 500
        assert "Network issue" in exc_info.value.message


@pytest.mark.asyncio
async def test_get_postgres_client_unknown_error():
    with patch('asyncpg.connect', new_callable=AsyncMock) as mock_connect:
        mock_connect.side_effect = Exception("Unknown error")
        with pytest.raises(CustomException) as exc_info:
            await get_postgres_client("test_db")
        assert exc_info.value.name == 'Error: Postgres connection'
        assert exc_info.value.error_code == 500
        assert "Failed to connect to the Postgres database: Unknown error" in exc_info.value.message




@pytest.mark.asyncio
async def test_get_user_data_from_database_success():
    user_data = {
        "username": "test_user",
        "role": "admin",
        "role_name": "Administrator",
        "created_at": "2023-01-01",
        "updated_at": "2023-01-02",
        "last_login": "2023-01-03"
    }
    
    with patch('services.postgres_connectors.get_postgres_client', new_callable=AsyncMock) as mock_get_client:
        mock_client = AsyncMock()
        mock_client.fetchrow.return_value = user_data
        mock_get_client.return_value = mock_client
        
        result = await get_user_data_from_database("test_user")
        
        assert result == user_data
        mock_client.fetchrow.assert_called_once_with(query_get_user_secure_data, "test_user")
        mock_client.close.assert_called_once()


@pytest.mark.asyncio
async def test_get_user_data_from_database_connection_error():
    with patch('services.postgres_connectors.get_postgres_client', new_callable=AsyncMock) as mock_get_client:
        mock_get_client.side_effect = CustomException("Error: Postgres connection", 500, "Connection error")
        
        with pytest.raises(CustomException) as exc_info:
            await get_user_data_from_database("test_user")
        
        assert exc_info.value.name == 'Error: Postgres connection'
        assert exc_info.value.error_code == 500
        assert "Connection error" in exc_info.value.message


@pytest.mark.asyncio
async def test_get_user_info_data_success():
    user_info = {
        "username": "test_user",
        "role": "admin",
        "role_name": "Administrator",
        "created_at": "2023-01-01",
        "updated_at": "2023-01-02",
        "last_login": "2023-01-03"
    }
    
    with patch('services.postgres_connectors.get_postgres_client', new_callable=AsyncMock) as mock_get_client:
        mock_client = AsyncMock()
        mock_client.fetchrow.return_value = user_info
        mock_get_client.return_value = mock_client
        
        result = await get_user_info_data("test_user")
        
        assert result == user_info
        mock_client.fetchrow.assert_called_once_with(query_get_user_info_data, "test_user")
        mock_client.close.assert_called_once()


@pytest.mark.asyncio
async def test_update_user_info_data_success():
    user_id_to_update = "test_user_id"
    info_to_update = {
        "role": "user",
        "last_login": "2023-01-04"
    }
    
    with patch('services.postgres_connectors.get_postgres_client', new_callable=AsyncMock) as mock_get_client:
        mock_client = AsyncMock()
        mock_client.fetchrow.return_value = None  # Simulate successful update
        mock_get_client.return_value = mock_client
        
        await update_user_info_data(user_id_to_update, info_to_update)
        
        mock_client.fetchrow.assert_called_once_with(query_update_user_info_data(user_id_to_update, info_to_update))
        mock_client.close.assert_called_once()


@pytest.mark.asyncio
async def test_check_if_user_exists_in_database_user_exists():
    with patch('services.postgres_connectors.get_postgres_client', new_callable=AsyncMock) as mock_get_client:
        mock_client = AsyncMock()
        mock_client.fetchrow.return_value = {"username": "test_user"}  # Simulate user exists
        mock_get_client.return_value = mock_client
        
        with pytest.raises(CustomException) as exc_info:
            await check_if_user_exists_in_database("test_user")
        
        assert exc_info.value.name == 'Register error'
        assert exc_info.value.error_code == 409
        assert "User already exists" in exc_info.value.message
        mock_client.fetchrow.assert_called_once_with(query_get_username, "test_user")
        mock_client.close.assert_called_once()


@pytest.mark.asyncio
async def test_force_verified_user_to_true_success():
    username_to_verify = "test_user"
    
    with patch('services.postgres_connectors.get_postgres_client', new_callable=AsyncMock) as mock_get_client:
        mock_client = AsyncMock()
        mock_client.execute.return_value = None  # Simulate successful execution
        mock_get_client.return_value = mock_client
        
        await force_verified_user_to_true(username_to_verify)
        
        mock_client.execute.assert_called_once_with(query_force_user_verified_true, username_to_verify)
        mock_client.close.assert_called_once()



@pytest.mark.asyncio
async def test_update_user_password_failure():
    user_who_updates = "test_user"
    new_password = Password(password="New_password123!!")
    hashed_password = "hashed_new_password"

    # Mock hash_string function
    with patch("utils.common_functions.hash_string", return_value=hashed_password):
        # Mock get_postgres_client function
        mock_client = AsyncMock()
        mock_client.execute = AsyncMock(side_effect=Exception("Database error"))
        mock_client.close = AsyncMock()
        with patch("services.postgres_connectors.get_postgres_client", return_value=mock_client):
            with pytest.raises(CustomException) as exc_info:
                await update_user_password(user_who_updates, new_password)

            # Assert exception message
            assert str(exc_info.value) == ""

            # Assert client was closed
            mock_client.close.assert_called_once()



@pytest.mark.asyncio
async def test_update_user_last_login_success():
    username = "test_user"
    
    with patch('services.postgres_connectors.get_postgres_client', new_callable=AsyncMock) as mock_get_client:
        mock_client = AsyncMock()
        mock_client.execute.return_value = None  # Simulate successful execution
        mock_get_client.return_value = mock_client
        
        await update_user_last_login(username)
        
        mock_client.execute.assert_called_once_with(query_update_user_last_login, username)
        mock_client.close.assert_called_once()


@pytest.mark.asyncio
async def test_update_user_last_login_failure():
    username = "test_user"
    
    with patch('services.postgres_connectors.get_postgres_client', new_callable=AsyncMock) as mock_get_client:
        mock_client = AsyncMock()
        mock_client.execute.side_effect = Exception("Database error")
        mock_get_client.return_value = mock_client
        
        with pytest.raises(CustomException) as exc_info:
            await update_user_last_login(username)
        
        assert exc_info.value.name == 'User last login error'
        assert exc_info.value.error_code == 500
        assert "Failed to update user last login date in the database: Database error" in exc_info.value.message
        mock_client.close.assert_called_once()