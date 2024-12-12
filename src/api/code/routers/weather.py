#api/routers/tester.py


# Lib
from fastapi import APIRouter, Depends, Request

from models.weather_base_models import WeatherRequest
from services.openmeteo import transform_and_return_openmeteoapi_response
from utils.common_functions import get_current_user
from utils.config import CURRENT_VERSION, TEST_LIMIT
from utils.decorators import require_role
from utils.exceptions import CustomException 
from utils.limiter import limiter


"""
Router Declaration
"""
weather = APIRouter()



"""
Routes Declaration
"""
@weather.post(f"/{CURRENT_VERSION}/weather/", tags = ["weather"])
@limiter.limit(TEST_LIMIT)
async def get_weather(user_params:WeatherRequest, request: Request, JWT_TOKEN: dict = Depends(get_current_user)):
    """
    Return Weather informations based on OpenMeteo API.

    Args:
    - user_params: WeatherRequest: Request type (forecast or archive), location, etc..

    Raises:
    - CustomException: Invalid request type

    Returns:
    - JSON: Weather information


    """
    if user_params.request_type in ["forecast", "archive"]:
        return transform_and_return_openmeteoapi_response(user_params)
    else:
        raise CustomException(name = "invalid_request",
                              error_code = 400,
                              message = "Invalid request type: Should be either 'forecast' or 'archive'")
