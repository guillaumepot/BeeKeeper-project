# api/unit_tests/redis_connectors_test.py
# export PYTHONPATH=$(pwd)

# Suppress DeprecationWarnings from passlib and crypt (python 1.13)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module='passlib')
warnings.filterwarnings("ignore", category=DeprecationWarning, module='crypt')


# Lib
import pytest
from unittest.mock import patch, MagicMock

from utils.exceptions import CustomException



# Functions to test
from services.redis_connectors import get_redis_client



@pytest.mark.asyncio
async def test_get_redis_client_success():
    with patch('redis.Redis') as MockRedis, \
         patch.dict('os.environ', {'REDIS_HOST': 'localhost', 'REDIS_PORT': '6379'}):
        mock_redis_instance = MagicMock()
        MockRedis.return_value = mock_redis_instance

        client = await get_redis_client()

        MockRedis.assert_called_once_with(host='localhost', port=6379, decode_responses=False)
        assert client == mock_redis_instance

@pytest.mark.asyncio
async def test_get_redis_client_failure():
    with patch('redis.Redis', side_effect=Exception('Connection error')), \
         patch.dict('os.environ', {'REDIS_HOST': 'localhost', 'REDIS_PORT': '6379'}):
        with pytest.raises(CustomException) as exc_info:
            await get_redis_client()

        assert exc_info.value.name == "Error: Redis connection"
        assert exc_info.value.error_code == 500
        assert "Failed to connect to the Redis database: Connection error" in exc_info.value.message