# api/unit_tests/user_objects_base_models_test.py
# export PYTHONPATH=$(pwd)

# Suppress DeprecationWarnings from passlib and crypt (python 1.13)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module='passlib')
warnings.filterwarnings("ignore", category=DeprecationWarning, module='crypt')



# Lib
import pytest
from uuid import UUID

from models.user_objects_base_models import Locations



# Test Locations base model
def test_valid_location():
    location = Locations(
        name="Test Location",
        commentary="Test Commentary",
        categories=["Category1", "Category2"],
        latitude=45.0,
        longitude=90.0
    )
    assert location.name == "Test Location"
    assert location.commentary == "Test Commentary"
    assert location.categories == ["Category1", "Category2"]
    assert location.latitude == 45.0
    assert location.longitude == 90.0

def test_invalid_latitude():
    with pytest.raises(ValueError):
        Locations(
            name="Test Location",
            latitude=100.0,  # Invalid latitude
            longitude=90.0
        )

def test_invalid_longitude():
    with pytest.raises(ValueError):
        Locations(
            name="Test Location",
            latitude=45.0,
            longitude=200.0  # Invalid longitude
        )

def test_default_optional_fields():
    location = Locations(
        name="Test Location",
        latitude=45.0,
        longitude=90.0
    )
    assert location.commentary == ""
    assert location.categories == []

def test_default_owner():
    location = Locations(
        name="Test Location",
        latitude=45.0,
        longitude=90.0
    )
    assert location.owner == None