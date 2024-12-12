# api/unit_tests/weather_base_models_test.py
# export PYTHONPATH=$(pwd)

# Suppress DeprecationWarnings from passlib and crypt (python 1.13)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module='passlib')
warnings.filterwarnings("ignore", category=DeprecationWarning, module='crypt')



# Lib
import pytest
from pydantic import ValidationError
from models.weather_base_models import WeatherRequest
from uuid import UUID

from models.user_objects_base_models import Locations



# Test Weather base model
def test_valid_weather_request():
    request = WeatherRequest(
        latitude=45.0,
        longitude=90.0,
        request_type="forecast",
        past_days=10,
        forecast_days=5,
        start_date="2023-01-01",
        end_date="2023-01-10"
    )
    assert request.latitude == 45.0
    assert request.longitude == 90.0
    assert request.request_type == "forecast"
    assert request.past_days == 10
    assert request.forecast_days == 5
    assert request.start_date == "2023-01-01"
    assert request.end_date == "2023-01-10"

def test_invalid_latitude():
    with pytest.raises(ValidationError):
        WeatherRequest(
            latitude=100.0,  # Invalid latitude
            longitude=90.0,
            request_type="forecast"
        )

def test_invalid_longitude():
    with pytest.raises(ValidationError):
        WeatherRequest(
            latitude=45.0,
            longitude=200.0,  # Invalid longitude
            request_type="forecast"
        )

def test_invalid_request_type():
    with pytest.raises(ValidationError):
        WeatherRequest(
            latitude=45.0,
            longitude=90.0,
            request_type="invalid_type"  # Invalid request type
        )

def test_invalid_date_format():
    with pytest.raises(ValidationError):
        WeatherRequest(
            latitude=45.0,
            longitude=90.0,
            request_type="forecast",
            start_date="01-01-2023"  # Invalid date format
        )

def test_missing_dates_for_archive():
    with pytest.raises(ValidationError):
        WeatherRequest(
            latitude=45.0,
            longitude=90.0,
            request_type="archive"  # Missing start_date and end_date
        )

def test_valid_forecast_request():
    request = WeatherRequest(
        latitude=45.0,
        longitude=90.0,
        request_type="forecast",
        forecast_days=5
    )
    assert request.request_type == "forecast"
    assert request.forecast_days == 5