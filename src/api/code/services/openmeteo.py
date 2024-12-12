# api/services/openmeteo.py


# Lib
import asyncio
import numpy as np
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

from models.weather_base_models import WeatherRequest
from services.redis_connectors import get_redis_client
from utils.config import forecast_url, historical_forecast_url, openmeteo_models, params_current_weather, params_daily_weather, params_hourly_weather
from utils.exceptions import CustomException


"""
FUNCTIONS
"""
async def setup_cache_session() -> requests_cache.CachedSession:
    redis_client = await get_redis_client()
    cache_session = requests_cache.CachedSession(
        backend = "redis",
        connection = redis_client,
        expire_after = 600
    )
    return cache_session


cache_session = asyncio.run(setup_cache_session())
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.5)
openmeteo = openmeteo_requests.Client(session = retry_session)


def request_openmeteo_api(user_params:WeatherRequest) -> dict:
    """
    
    """
    params = {
        "latitude": user_params.latitude,
        "longitude": user_params.longitude,
        "daily": params_daily_weather,
        "hourly": params_hourly_weather,
        "models": openmeteo_models,
    }


    if user_params.request_type == "forecast":
        params["current"] = params_current_weather
        params["past_days"] = user_params.past_days
        params["forecast_days"] = user_params.forecast_days

        url = forecast_url

    else:
        params["start_date"] = user_params.start_date
        params["end_date"] = user_params.end_date

        url = historical_forecast_url


    responses = openmeteo.weather_api(url, params = params)
    response = responses[0]

    return response



def transform_and_return_openmeteoapi_response(user_params:WeatherRequest) -> dict:
    """
    Transform and return OpenMeteo API response to a JSON format.
    """
    response = request_openmeteo_api(user_params)

    # Transform daily
    daily = response.Daily()

    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}


    for index, elt in enumerate(params_daily_weather):
        daily_data[elt] = daily.Variables(index).ValuesAsNumpy()


    for key, value in daily_data.items():
        if isinstance(value, list) or isinstance(value, int):
            pass
        else:
            daily_data[key] = value.tolist()


    # Transform hourly
    hourly = response.Hourly()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}


    for index, elt in enumerate(params_hourly_weather):
        values = hourly.Variables(index).ValuesAsNumpy()
        hourly_data[elt] = [None if np.isnan(v) else v for v in values]


    for key, value in hourly_data.items():
        if isinstance(value, int) or isinstance(value, list):
            pass
        else:
            hourly_data[key] = value.tolist()
            
        hourly_data[key] = [float(v) if isinstance(v, np.float32) else v for v in value]



    # Transform current
    if user_params.request_type == "forecast":
        current = response.Current()
        transformed_current = {}

        for index, elt in enumerate(params_current_weather):
            transformed_current[f"current_{elt}"] = current.Variables(index).Value()

        return transformed_current, daily_data, hourly_data
    
    else:
        return daily_data, hourly_data
