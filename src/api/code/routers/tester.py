#api/routers/tester.py


# Lib
from fastapi import APIRouter, Depends, Request

from utils.common_functions import get_current_user
from utils.config import CURRENT_VERSION, TEST_LIMIT
from utils.decorators import require_role
from utils.exceptions import CustomException 
from utils.limiter import limiter


"""
Router Declaration
"""
tester = APIRouter()



"""
Routes Declaration
"""

# Raises an exception
@tester.get(f"/{CURRENT_VERSION}/test/exception", tags = ["debug"])
def get_my_custom_exception():
    raise CustomException(name = "test_error", error_code = 500, message = "This is a test error")


# Teturns a response without login
@tester.get(f"/{CURRENT_VERSION}/test/hello", tags = ["debug"])
def get_hello():
    return {"message": "Hello World!"}


# Limiter testing
@tester.get(f"/{CURRENT_VERSION}/test/limited_hello", tags = ["debug"])
@limiter.limit(TEST_LIMIT)
def get_limited_hello(request: Request, JWT_TOKEN:dict = Depends(get_current_user)):
    return {"message": "Limited Hello! You can only access this route 3 times per minute"}


# Route that returns a response with login
@tester.get(f"/{CURRENT_VERSION}/test/secured_hello", tags = ["debug"])
def get_secured_hello(JWT_TOKEN:dict = Depends(get_current_user)):
    return {"message": f"[Secured] Hello {JWT_TOKEN['username']}!, your informations: {JWT_TOKEN}"}


# Route that requires a specific role
@tester.get(f"/{CURRENT_VERSION}/test/role_hello", tags = ["debug"])
@require_role(role = "admin")
def get_role_hello(JWT_TOKEN:dict = Depends(get_current_user)):
    return {"message": f"[Role] Hello {JWT_TOKEN['username']}, your role is {JWT_TOKEN['role_name']}"}

