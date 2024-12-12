#api/routers/cartographic.py




# Lib
from fastapi import APIRouter, Depends, Request

from models.params_emplacements_base_model import ParamsLocation
from services.auth import get_current_user
from services.postgres_connectors import get_carto_from_database
from utils.config import CURRENT_VERSION, CARTO_LIMIT
from utils.limiter import limiter


"""
Router Declaration
"""
cartographic = APIRouter()




"""
Routes Declaration
"""
@cartographic.post(f"/{CURRENT_VERSION}/carto", tags = ["cartographic"])
async def get_carto(locations: list[ParamsLocation]):
    """
    Get the carto data depending on the locations
    """
    data:dict = {}

    for location in locations:
        data[location.location_name] = await get_carto_from_database(location)

    return data