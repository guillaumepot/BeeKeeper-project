#models/user_objects_base_models.py


# Lib
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, PrivateAttr, field_validator
from typing import Optional, List
from uuid import uuid4, UUID

from utils.exceptions import CustomException




# BASE MODELS
class Locations(BaseModel):
    name: str
    commentary: Optional[str] = ""
    categories: Optional[List[str]] = []
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

    # Default values set by the system
    owner: Optional[UUID] = None



class Hives(BaseModel):
    name: str
    # Default values set by the system
    owner: Optional[UUID] = None
    location_name: Optional[str] = None  # Ajout d'un champ pour le nom de la location