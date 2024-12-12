#models/weather_base_models.py


# Lib
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, field_validator, model_validator



# BASE MODELS
class WeatherRequest(BaseModel):
    latitude:float = Field(..., ge=-90, le=90)
    longitude:float = Field(..., ge=-180, le=180)
    request_type: Literal["forecast", "archive"] = "forecast"  # Force only 2 possible values
    past_days:int = Field(0, ge=0, le=92)           # 3 months max based on OpenMeteoAPI
    forecast_days:int = Field(0, ge=0, le=16)       # 16 days max based on OpenMeteoAPI
    start_date:str = None
    end_date:str = None

    @field_validator("request_type")
    def to_lowercase(cls, value: str) -> str:
        return value.lower()
    
    @field_validator("start_date", "end_date")
    def validate_date_format(cls, value: str) -> str:
        if value is None:
            return value
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Date '{value}' is not in the format 'yyyy-mm-dd'")
        return value
    
    @model_validator(mode='after')
    def check_dates_if_archive(cls, values):
        if values.request_type == "archive":
            if not values.start_date or not values.end_date:
                raise ValueError("start_date and end_date must be provided when request_type is 'archive'")
        return values