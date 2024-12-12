# api/unit_tests/params_emplacements_base_model_test.py
# export PYTHONPATH=$(pwd)

# Suppress DeprecationWarnings from passlib and crypt (python 1.13)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module='passlib')
warnings.filterwarnings("ignore", category=DeprecationWarning, module='crypt')



# Lib
import pytest
from uuid import UUID

from models.params_emplacements_base_model import ParamsLocation
from utils.exceptions import CustomException


# Test ParamsLocations base model
def test_params_location_valid_data():
    data = {
        "location_name": "Test Location",
        "latitude": 45.0,
        "longitude": 90.0,
        "data_type": ["rpg"],
        "years": [2020, 2021],
        "radius": 100
    }
    location = ParamsLocation(**data)
    assert location.location_name == "Test Location"
    assert location.latitude == 45.0
    assert location.longitude == 90.0
    assert location.data_type == ["rpg"]
    assert location.years == [2020, 2021]
    assert location.radius == 100

def test_params_location_invalid_latitude():
    data = {
        "location_name": "Test Location",
        "latitude": 100.0,  # Invalid latitude
        "longitude": 90.0,
        "data_type": ["rpg"],
        "years": [2020, 2021],
        "radius": 100
    }
    with pytest.raises(ValueError):
        ParamsLocation(**data)

def test_params_location_invalid_longitude():
    data = {
        "location_name": "Test Location",
        "latitude": 45.0,
        "longitude": 200.0,  # Invalid longitude
        "data_type": ["rpg"],
        "years": [2020, 2021],
        "radius": 100
    }
    with pytest.raises(ValueError):
        ParamsLocation(**data)

def test_params_location_invalid_data_type():
    data = {
        "location_name": "Test Location",
        "latitude": 45.0,
        "longitude": 90.0,
        "data_type": ["invalid_type"],  # Invalid data type
        "years": [2020, 2021],
        "radius": 100
    }
    with pytest.raises(CustomException) as excinfo:
        ParamsLocation(**data)
    assert excinfo.value.name == "data_type_error"
    assert excinfo.value.error_code == 422

def test_params_location_missing_years_for_rpg():
    data = {
        "location_name": "Test Location",
        "latitude": 45.0,
        "longitude": 90.0,
        "data_type": ["rpg"],  # RPG data type requires years
        "radius": 100
    }
    with pytest.raises(CustomException) as excinfo:
        ParamsLocation(**data)
    assert excinfo.value.name == "year_error"
    assert excinfo.value.error_code == 422