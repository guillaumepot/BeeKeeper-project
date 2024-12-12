#models/weather_base_models.py


# Lib
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

from utils.config import AVAILABLE_DATA_TYPES
from utils.exceptions import CustomException




# BASE MODELS
class ParamsLocation(BaseModel):
    location_name:str = Field("location", min_length=1, max_length=100)
    latitude:float = Field(..., ge=-90, le=90)
    longitude:float = Field(..., ge=-180, le=180)
    data_type: List[str] = []
    years: Optional[list[int]] = None
    radius:float = Field(50, ge=50, le=5000)



    @field_validator("data_type")
    def validate_data_type(cls, values:list[str]) -> list:
        """
        Control data type values
        """
        for value in values:
            if value not in AVAILABLE_DATA_TYPES:
                raise CustomException(name = "data_type_error",
                                      error_code = 422,
                                      message = "Data type error.")
        return values


    def __init__(self, **data):
        super().__init__(**data)
        if "rpg" in AVAILABLE_DATA_TYPES and self.years is None:
            raise CustomException(name = "year_error",
                                  error_code = 422,
                                  message = "a list of years is required for RPG data type.")