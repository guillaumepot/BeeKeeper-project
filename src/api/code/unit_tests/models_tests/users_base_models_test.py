# api/unit_tests/users_base_models_test.py
# export PYTHONPATH=$(pwd)

# Suppress DeprecationWarnings from passlib and crypt (python 1.13)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module='passlib')
warnings.filterwarnings("ignore", category=DeprecationWarning, module='crypt')



# Lib
import pytest
from datetime import datetime
from uuid import UUID

from utils.exceptions import CustomException
from models.users_base_models import Password, User, UserInfos




# Functions to test Password model
def test_valid_password():
    password = Password(password="Valid1Password!")
    assert password.password == "Valid1Password!"

def test_password_without_digit():
    with pytest.raises(CustomException) as excinfo:
        Password(password="NoDigitPassword!")
    assert excinfo.value.name == "password_digit_error"
    assert excinfo.value.error_code == 422

def test_password_without_uppercase():
    with pytest.raises(CustomException) as excinfo:
        Password(password="nouppercase1!")
    assert excinfo.value.name == "password_uppercase_error"
    assert excinfo.value.error_code == 422

def test_password_without_lowercase():
    with pytest.raises(CustomException) as excinfo:
        Password(password="NOLOWERCASE1!")
    assert excinfo.value.name == "password_lowercase_error"
    assert excinfo.value.error_code == 422

def test_password_without_special_char():
    with pytest.raises(CustomException) as excinfo:
        Password(password="NoSpecialChar1")
    assert excinfo.value.name == "password_special_char_error"
    assert excinfo.value.error_code == 422

# Functions to test User model
def test_valid_user():
    user = User(username="ValidUser", password=Password(password="Valid1Password!"), email="USER@EXAMPLE.COM")
    assert user.username == "validuser"
    assert user.email == "user@example.com"
    assert isinstance(user._id, UUID)
    assert user._role == 1
    assert user._verified == False
    assert isinstance(user._created_at, datetime)
    assert isinstance(user._updated_at, datetime)
    assert isinstance(user._last_login, datetime)

def test_user_read_only_attributes():
    user = User(username="ValidUser", password=Password(password="Valid1Password!"), email="user@example.com")
    with pytest.raises(AttributeError):
        user._id = UUID("12345678123456781234567812345678")
    with pytest.raises(AttributeError):
        user._role = 2
    with pytest.raises(AttributeError):
        user._verified = True
    with pytest.raises(AttributeError):
        user._created_at = datetime.now()
    with pytest.raises(AttributeError):
        user._updated_at = datetime.now()
    with pytest.raises(AttributeError):
        user._last_login = datetime.now()

# Functions to test UserInfos model
def test_valid_userinfos():
    user_infos = UserInfos(address="123 Main St", zipcode="12345", city="Anytown", country="USA", phone="123-456-7890", email="USER@EXAMPLE.COM")
    assert user_infos.address == "123 Main St"
    assert user_infos.zipcode == "12345"
    assert user_infos.city == "Anytown"
    assert user_infos.country == "USA"
    assert user_infos.phone == "123-456-7890"
    assert user_infos.email == "user@example.com"

def test_userinfos_remove_none_attributes():
    user_infos = UserInfos(address=None, zipcode="12345", city=None, country="USA", phone=None, email="user@example.com")
    assert not hasattr(user_infos, 'address')
    assert user_infos.zipcode == "12345"
    assert not hasattr(user_infos, 'city')
    assert user_infos.country == "USA"
    assert not hasattr(user_infos, 'phone')
    assert user_infos.email == "user@example.com"