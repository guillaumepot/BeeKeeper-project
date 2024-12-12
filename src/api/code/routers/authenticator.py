#api/routers/authenticator.py


# Lib
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm


from models.users_base_models import User
from services.auth import verify_credentials, encode_jwt
from services.postgres_connectors import get_user_data_from_database, check_if_user_exists_in_database, register_user_in_database, update_user_last_login
from utils.exceptions import CustomException 
from utils.limiter import limiter




"""
Router Declaration
"""
authenticator = APIRouter()



"""
Routes Declaration
"""
@authenticator.post("/login", tags = ["auth"])
async def login(request: Request, credentials: OAuth2PasswordRequestForm = Depends()):
    """
    Login route
    """
    await verify_credentials(credentials.username, credentials.password)

    await update_user_last_login(credentials.username)

    user_data = await get_user_data_from_database(credentials.username)

    return {"access_token": encode_jwt(**user_data), "token_type": "bearer"}



@authenticator.post("/register", tags = ["auth"])
async def register(request: Request, new_user:User):

    try:        
        await check_if_user_exists_in_database(new_user.username)
            
    except CustomException as e:
        raise CustomException(name = "Check Username returns error", error_code = e.error_code, message = e.message)
    
    else:
        await register_user_in_database(new_user)
        return {"message": f"{new_user.username.lower()} has been registered!"}