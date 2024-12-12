#api/utils/common_functions.py


# Lib
from utils.config import PWD_CONTEXT
import logging
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from utils.exceptions import CustomException
import jwt
from utils.config import JWT_SECRET_KEY, ENCODING_ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    - Decode the JWT token and return the token

    Args:
        - token (str): The JWT token

    Raises:
        - CustomException if the token is invalid

    Returns:
        - The decoded token
    """
    try:
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=ENCODING_ALGORITHM)
    except Exception as e:
        raise CustomException(name='Auth_token_error', error_code=500, message="Invalid token") from e
    return decoded_token





def hash_string(string_to_hash:str) -> str:
    """
    - Hash a string using the pwd_context hash algorithm

    Args:
        - string_to_hash (str): The string to hash

    Returns:
        - The hashed string
    """
    return PWD_CONTEXT.hash(string_to_hash)



def get_jwt_token(request: Request) -> str:
    """
    Extract the JWT token from the request headers.
    """
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token[len("Bearer "):]

    try:
        decoded_token = get_current_user(token = token)
    except CustomException as e:
        raise e
    else:
        return decoded_token
    


def get_projection(lat:float, lon:float) -> int:
    """
    Return SRID code
    """
    # Reunion
    if lat < -20.8 and lat > -21.5 and lon < 56 and lon > 55:
        return 2975
    
    # Martinique
    if lon < -60 and lon > -61.5 and lat < 15 and lat > 14:
        return 5490

    # Guadeloupe
    if lon < -60.5 and lon > -62 and lat < 16.6 and lat > 15.8:
        return 5490

    # Guyane
    if lon < -51.1 and lon > -55.5 and lat < 6 and lat > 2:
        return 2972


    # Mayotte
    if lon < 45.5 and lon > 44.5 and lat < -12 and lat > -13:
        return 4471
 
    # Metropole
    if lat < 52 and lat > 38 and lon < 11 and lon > -7:
        return 2154

    else:
        return 2154