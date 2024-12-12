# api/unit_tests/utils_tests/decorators_tests.py
# export PYTHONPATH=$(pwd)

# Suppress DeprecationWarnings from passlib and crypt (python 1.13)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module='passlib')
warnings.filterwarnings("ignore", category=DeprecationWarning, module='crypt')


# Lib
import pytest

from utils.exceptions import CustomException
from utils.decorators import require_role



# Functions to test
exception = CustomException(name = ' Auth_role_error',
                            error_code = 401,
                            message = "You do not have the required permissions to access this route.")


@pytest.mark.asyncio
async def test_require_role_async_success():
    @require_role('admin')
    async def mock_func(*args, **kwargs):
        return "Success"

    result = await mock_func(JWT_TOKEN={'role_name': 'admin'})
    assert result == "Success"

@pytest.mark.asyncio
async def test_require_role_async_failure():
    @require_role('admin')
    async def mock_func(*args, **kwargs):
        return "Success"

    with pytest.raises(CustomException) as exc_info:
        await mock_func(JWT_TOKEN = {'role_name': 'user'})
    assert exc_info.value.name == 'Auth_role_error'
    assert exc_info.value.error_code == 401
    assert exc_info.value.message == "You do not have the required permissions to access this route."

def test_require_role_sync_success():
    @require_role('admin')
    def mock_func(*args, **kwargs):
        return "Success"

    result = mock_func(JWT_TOKEN={'role_name': 'admin'})
    assert result == "Success"

def test_require_role_sync_failure():
    @require_role('admin')
    def mock_func(*args, **kwargs):
        return "Success"

    with pytest.raises(CustomException) as exc_info:
        mock_func(JWT_TOKEN={'role_name': 'user'})
    assert exc_info.value.name == 'Auth_role_error'
    assert exc_info.value.error_code == 401
    assert exc_info.value.message == "You do not have the required permissions to access this route."