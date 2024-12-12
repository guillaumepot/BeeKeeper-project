#models/users_base_models.py


# Lib
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, PrivateAttr, field_validator
from typing import Optional
from uuid import uuid4, UUID

from utils.exceptions import CustomException



# BASE MODELS
class Password(BaseModel):
    password: str = Field(..., min_length = 8 , max_length = 40)


    @field_validator("password")
    def validate_password(cls, value:str) -> str:
        """
        Check pasword complexity using conditions:
        - At least one digit
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one special character: !?@#$%^&*()_+
        """
        if not any(char.isdigit() for char in value):
            raise CustomException(name = "password_digit_error", error_code = 422, message="Password must contain at least one number")
        if not any(char.isupper() for char in value):
            raise CustomException(name = "password_uppercase_error", error_code = 422, message = "Password must contain at least one uppercase letter")
        if not any(char.islower() for char in value):
            raise CustomException(name = "password_lowercase_error", error_code = 422, message = "Password must contain at least one lowercase letter")
        if not any(char in "!?@#$%^&*()_+" for char in value):
            raise CustomException(name = "password_special_char_error", error_code=422, message = "Password must contain at least one special character: !?@#$%^&*()_+")
        return value




class User(BaseModel):
    # Created by the user
    username: str = Field(..., min_length = 6, max_length = 25)   # ... -> required (no optional)
    password: Password
    email: EmailStr


    # Default values set by the system
    _id: UUID = PrivateAttr(default_factory = uuid4)
    _role: int = PrivateAttr(default = 1)
    _verified: bool = PrivateAttr(default = False)
    _created_at: datetime = PrivateAttr(default_factory = datetime.now)
    _updated_at: datetime = PrivateAttr(default_factory = datetime.now)
    _last_login: datetime = PrivateAttr(default_factory=  datetime.now)


    @field_validator("username", "email")
    def to_lowercase(cls, value: str) -> str:
        return value.lower()



    def __setattr__(self, attribute, value):
        """
        Override __setattr__ to prevent modification of defined attributes below.
        """
        if attribute in ["_id", "_role", "_verified", "_created_at", "_updated_at", "_last_login"]:
            raise AttributeError("Attribute value is read-only")
        super().__setattr__(attribute, value)



class UserInfos(BaseModel):
    # Updated by the user
    address: Optional[str] = None
    zipcode: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


    def __init__(self, **data):
        """
        Constructor
        - Convert email to lowercase
        - Remove attributes that are None
        """
        super().__init__(**data)
        if self.email:
            self.email = self.email.lower()

        # Remove attributes that are None
        for attr, value in list(self.__dict__.items()):
            if value is None:
                delattr(self, attr)