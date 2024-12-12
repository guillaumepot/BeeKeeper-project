# api/services/auth.py


# Lib
from datetime import datetime, timedelta
from fastapi import Depends
import jwt # PyJWT library


from services.postgres_connectors import get_postgres_client
from utils.common_functions import oauth2_scheme
from utils.config import ACCESS_TOKEN_EXPIRATION_IN_MINUTES, JWT_SECRET_KEY, ENCODING_ALGORITHM, USER_DATABASE, PWD_CONTEXT
from utils.exceptions import CustomException 
from utils.postgres_requests.user_requests import query_get_user_credentials_in_database







def verify_password(given_password:str, hashed_password:str) -> None:
    """
    - Verify if the given password matches the hashed password

    Args:
        - given_password (str): The password given by the user
        - hashed_password (str): The hashed password stored in the database
    """
    if PWD_CONTEXT.verify(given_password, hashed_password) == False:
        raise CustomException(name='Auth_password_error', error_code=401, message="Incorrect password")



async def verify_credentials(given_username:str, given_password:str) -> None:
    """
    - Request a Postgres connection to verify the credentials of a user
    - Search for user in the databse and then compare credentials. Account has to be verified

    Args:
        - credentials (dict): The username and password of the user (OAuth2PasswordRequestForm)
    
    Raises:
        - CustomException if the username is not found in the database
        - CustomException if the account is not verified
        - CustomException if the password is incorrect
    """
    # Search for user in the database
    client = await get_postgres_client(database = USER_DATABASE)
    user_credentials_in_database = await client.fetchrow(query_get_user_credentials_in_database, given_username)
    # Controls (username, password matching, verified account)
    if user_credentials_in_database is None:
        raise CustomException(name='Auth_username_error', error_code=401, message="Username not found in the database")
    elif user_credentials_in_database["verified"] != True:
        raise CustomException(name='Auth_verification_error', error_code=401, message="Account not verified")
    else:
        try:
            verify_password(given_password, user_credentials_in_database["password"])
        except CustomException as e:
            raise e
        finally:
            await client.close()



def encode_jwt(**data_to_encode) -> str:
    """
    - Encode data to a JWT token with specified secret key and encoding algorithm

    Args:
        - data_to_encode (dict): Data to encode in the JWT token
    
    Returns:
        - Encoded JWT token
    
    """

    # Set expiration time
    for key, value in data_to_encode.items():
        if isinstance(value, datetime):
            data_to_encode[key] = value.isoformat()


    token_expiration = timedelta(minutes=ACCESS_TOKEN_EXPIRATION_IN_MINUTES)
    data_to_encode["exp"] = datetime.now() + token_expiration 

    # Return encoded JWT
    return jwt.encode(payload = data_to_encode, key = JWT_SECRET_KEY, algorithm = ENCODING_ALGORITHM)



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