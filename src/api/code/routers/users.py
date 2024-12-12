#api/routers/postgres_users.py


# Lib
from fastapi import APIRouter, Depends, Request

from models.user_objects_base_models import Locations
from models.user_objects_base_models import Hives
from models.users_base_models import UserInfos, Password
from services.auth import verify_credentials
from services.mongodb_connectors import request_user_locations
from services.mongodb_connectors import request_user_hives
from services.postgres_connectors import force_verified_user_to_true, get_user_info_data, update_user_info_data, update_user_password
from utils.common_functions import get_current_user
from utils.config import CURRENT_VERSION, INSERT_INFOS_LIMIT, UPDATE_INFOS_LIMIT, PASSWORD_UPDATE_LIMIT, USER_LOCATIONS_LIMIT, USER_HIVES_LIMIT
from utils.decorators import require_role
from utils.exceptions import CustomException
from utils.limiter import limiter




"""
Router Declaration
"""
users_router = APIRouter()



"""
Routes Declaration
"""
@users_router.get(f"/{CURRENT_VERSION}/users/infos/", tags = ["users"])
@limiter.limit(INSERT_INFOS_LIMIT)
async def get_user_info(request: Request, JWT_TOKEN: dict = Depends(get_current_user)):
    """
    Retrieve user informations from the database
    """
    current_user_infos = await get_user_info_data(JWT_TOKEN["username"])
    return current_user_infos



@users_router.post(f"/{CURRENT_VERSION}/users/infos/", tags = ["users"])
@limiter.limit(UPDATE_INFOS_LIMIT)
async def post_user_info(update: UserInfos, request: Request, JWT_TOKEN: dict = Depends(get_current_user)):
    """
    POST method of the previous route to update user info (instead of GET)
    """
    updated_informations:dict = {}

    for key, value in update.dict().items():
        if value is not None:
            updated_informations[key] = value

    await update_user_info_data(user_id_to_update = JWT_TOKEN["id"],
                                info_to_update = updated_informations)
    
    return {"message": f"User {JWT_TOKEN["username"]} informations have been updated"}



@users_router.post(f"/{CURRENT_VERSION}/users/password/update/", tags = ["users"])
@limiter.limit(PASSWORD_UPDATE_LIMIT)
async def update_user_pasword(current_password:str, new_password:Password, request: Request, JWT_TOKEN: dict = Depends(get_current_user)):
    """
    Update user password in the database (requires current password)
    """
    try:
        await verify_credentials(JWT_TOKEN["username"], current_password)
        await update_user_password(JWT_TOKEN["username"], new_password)
        return {"message": "Password has been updated"}
    except CustomException as e:
        raise e



@users_router.put(f"/{CURRENT_VERSION}/users/force_verified/", tags = ["users"])
@require_role(role = "admin")
async def force_verified_to_true(request: Request, username_to_verify: str, JWT_TOKEN: dict = Depends(get_current_user)):
    """
    Change verified field to True for a specific user (requires admin rights)

    Args:
        - username_to_verify (str): The username of the user to verify
        - JWT_TOKEN (dict): The user data (from JWT token)

    Raises:
        - CustomException: If the user doesn't exist in the database
        - CustomException: If the force verification function fails

    Returns:
        - dict: A message confirming the action
    """
    username_to_verify = username_to_verify.lower()
    try:
        await force_verified_user_to_true(username_to_verify)
        return {"message": f"User {username_to_verify} has been manually verified by {JWT_TOKEN["username"]}"}
    except CustomException as e:
        raise e
    


@users_router.get(f"/{CURRENT_VERSION}/users/locations/", tags = ["users"])
@limiter.limit(USER_LOCATIONS_LIMIT)
async def get_user_locations(request: Request, JWT_TOKEN: dict = Depends(get_current_user)):
    """
    Retrieve user locations from the MongoDB database
    """
    return await request_user_locations(user_id = JWT_TOKEN["id"], method = "GET")



@users_router.post(f"/{CURRENT_VERSION}/users/locations/", tags = ["users"])
@limiter.limit(USER_LOCATIONS_LIMIT)
async def post_user_locations(location: Locations, request: Request, JWT_TOKEN: dict = Depends(get_current_user)):
    """
    Add user locations from the MongoDB database
    """
    location.owner = JWT_TOKEN["id"]
    return await request_user_locations(method = "POST", location = location)



@users_router.put(f"/{CURRENT_VERSION}/users/locations/", tags = ["users"])
@limiter.limit(USER_LOCATIONS_LIMIT)
async def update_user_locations(location: Locations, request: Request, JWT_TOKEN: dict = Depends(get_current_user)):
    """
    Update user locations from the MongoDB database
    """
    location.owner = JWT_TOKEN["id"]
    return await request_user_locations(method = "PUT", location = location)



@users_router.delete(f"/{CURRENT_VERSION}/users/locations/", tags = ["users"])
@limiter.limit(USER_LOCATIONS_LIMIT)
async def delete_user_locations(location_id: str, request: Request, JWT_TOKEN: dict = Depends(get_current_user)):
    """
    Delete user locations from the MongoDB database
    """
    user_locations = await request_user_locations(user_id = JWT_TOKEN["id"], method = "GET")

    # Find the location in the user locations correspond to location_id:
    if location_id in [location["_id"] for location in user_locations]:
        location_dict = user_locations[[location["_id"] for location in user_locations].index(location_id)]
        location = Locations(**location_dict)
        return await request_user_locations(method = "DELETE", location = location)
    else:
        raise CustomException(
            name = "Error: MongoDB collection",
            error_code = 404,
            message = f"Location {location_id} not found for user {JWT_TOKEN['username']}"
        )



@users_router.get(f"/{CURRENT_VERSION}/users/hives/", tags = ["users"])
@limiter.limit(USER_HIVES_LIMIT)
async def get_user_hives(request: Request, JWT_TOKEN: dict = Depends(get_current_user)):
    """
    Retrieve user hives from the MongoDB database
    """
    return await request_user_hives(user_id = JWT_TOKEN["id"], method = "GET")



@users_router.post(f"/{CURRENT_VERSION}/users/hives/", tags = ["users"])
@limiter.limit(USER_HIVES_LIMIT)
async def post_user_hives(hive: Hives, request: Request, JWT_TOKEN: dict = Depends(get_current_user)):
    """
    Add user hives from the MongoDB database
    """
    hive.owner = JWT_TOKEN["id"]
    return await request_user_hives(method = "POST", hive = hive)



@users_router.put(f"/{CURRENT_VERSION}/users/hives/", tags=["users"])
@limiter.limit(USER_LOCATIONS_LIMIT)
async def update_user_hives(hive: Hives, request: Request, JWT_TOKEN: dict = Depends(get_current_user)):
    """
    Update user hives from the MongoDB database
    """
    hive.owner = JWT_TOKEN["id"]
    return await request_user_hives(method="PUT", hive=hive)



@users_router.delete(f"/{CURRENT_VERSION}/users/hives/", tags=["users"])
@limiter.limit(USER_HIVES_LIMIT)
async def delete_user_hives(hive_id: str, request: Request, JWT_TOKEN: dict = Depends(get_current_user)):
    """
    Delete user hives from the MongoDB database
    """
    user_hives = await request_user_hives(user_id=JWT_TOKEN["id"], method="GET")

    # Find the hive in the user hives correspond to hive_id:
    if hive_id in [hive["_id"] for hive in user_hives]:
        hive_dict = user_hives[[hive["_id"] for hive in user_hives].index(hive_id)]
        hive = Hives(**hive_dict)
        return await request_user_hives(method="DELETE", hive=hive)