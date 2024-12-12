# api/utils/excedecorators.py


# Lib
import asyncio
from functools import wraps


from utils.exceptions import CustomException


exception = CustomException(name = "Auth_role_error",
                            error_code = 401,
                            message = "You do not have the required permissions to access this route.")



"""
DECORATORS
"""
def require_role(role: str):
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            user_data = kwargs.get("JWT_TOKEN")
            if not user_data or user_data.get("role_name") != role:
                raise exception
            return await func(*args, **kwargs)

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            user_data = kwargs.get("JWT_TOKEN")
            if not user_data or user_data.get("role_name") != role:
                raise exception
            return func(*args, **kwargs)

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator