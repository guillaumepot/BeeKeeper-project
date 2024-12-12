# api/services/postgres_connectors.py


# Lib
import asyncpg

from uuid import UUID
import shapely.wkb



from models.params_emplacements_base_model import ParamsLocation
from models.users_base_models import User, Password
from utils.config import POSTGRES_API_USER, POSTGRES_API_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, USER_DATABASE, CARTO_DATABASE
from utils.exceptions import CustomException
from utils.common_functions import hash_string, get_projection


# SELECT queries
from utils.postgres_requests.user_requests import query_get_username, query_get_user_secure_data, query_get_user_info_data
from utils.postgres_requests.cartographic_requests import query_get_rpg_location, query_get_clc_location
# from utils.postgres_requests.cartographic_requests import query_get_foretV2_location
# INSERT queries
from utils.postgres_requests.user_requests import query_insert_new_user, query_insert_user_log, query_insert_user_info
# UPDATE queries
from utils.postgres_requests.user_requests import query_update_user_password, query_update_user_last_login, query_force_user_verified_true, query_update_user_info_data





# Functions
async def get_postgres_client(database:str) -> asyncpg.Connection:
    """
    Get a connection to the Postgres database.

    Args:
        - database (str): The name of the database to connect to
    Returns:
        - A connection to the Postgres database (client)

    Raises:
        - CustomException if the connection fails
    """
    try:
        client = await asyncpg.connect(user = POSTGRES_API_USER,
                                       password = POSTGRES_API_PASSWORD,
                                       database = database,
                                       host = POSTGRES_HOST,
                                       port = POSTGRES_PORT
                                      )
    
    except Exception as e:
        raise CustomException(name = "Error: Postgres connection",
                              error_code = 500,
                              message = f"Failed to connect to the Postgres database: {e}")


    else:
        return client
    


async def get_user_data_from_database(username:str) -> dict:
    """
    Get user datas user for the sessions from the database.

    Args:
        - username (str): The username of the user
    
    Returns:
        - A dictionary containing the user data (username, role, role_name, created_at, updated_at, last_login)
    """
    try:
        client = await get_postgres_client(database = USER_DATABASE)
    except Exception as e:
        raise CustomException(name = "Error: Postgres connection",
                              error_code = 500,
                              message = f"Failed to connect to the Postgres database: {e}")
    else:
        user_data = await client.fetchrow(query_get_user_secure_data, username)
        # Convert UUIDs to strings
        user_data = {k: str(v) if isinstance(v, UUID) else v for k, v in user_data.items()}
        await client.close()

    return user_data



async def get_user_info_data(username:str) -> dict:
    """
    Get user information from the database.

    Args:
        - username (str): The username of the user

    Returns:
        - A dictionary containing the user info data (username)
    """
    try:
        client = await get_postgres_client(database = USER_DATABASE)
    except Exception as e:
        raise CustomException(name = "Error: Postgres connection",
                              error_code = 500,
                              message = f"Failed to connect to the Postgres database: {e}")
    else:
        user_info = await client.fetchrow(query_get_user_info_data, username)
        await client.close()
        
    return user_info



async def update_user_info_data(user_id_to_update:str, info_to_update:dict) -> None:
    """
    Update user informations (table user_infos) in the database.

    Args:
        - user_id_to_update (str): The user id to update
        - info_to_update (dict): The informations to update

    Raises:
        - CustomException: If the update fails
    """
    try:
        client = await get_postgres_client(database = USER_DATABASE)
    except Exception as e:
        raise CustomException(name = "Error: Postgres connection",
                              error_code = 500,
                              message = f"Failed to connect to the Postgres database: {e}")
    else:
        await client.fetchrow(query_update_user_info_data(user_id_to_update, info_to_update))
        await client.close()



async def check_if_user_exists_in_database(username:str) -> None:
    """
    Check if the user exists in the database.

    Args:
        - username (str): The username of the user

    Raises:
        - CustomException: If the user already exists in the database
    """
    client = await get_postgres_client(database=USER_DATABASE)
    try:
        user_data = await client.fetchrow(query_get_username, username)
        if user_data is not None:
            raise CustomException(name="Register error",
                                  error_code=409,
                                  message="User already exists")
    finally:
        await client.close()



async def force_verified_user_to_true(username_to_verify:str) -> None:
    """
    Change the value of the verified field to True for a specific user.

    Args:
        - username_to_verify (str): The username of the user to verify

    Raises:
        - CustomException: If the user doesn't exist in the database
        - CustomException: If the force verification function fails
    """
    client = await get_postgres_client(database = USER_DATABASE)

    try:
        await client.execute(query_force_user_verified_true, username_to_verify)
    except Exception as e:
        raise CustomException(name = "Force verified error", 
                              error_code = 500,
                              message = f"Failed to force verify the user: {e}")
    finally:
        await client.close()



async def register_user_in_database(new_user:User) -> None:
    """
    Register a new user in the database.

    Args:
        - new_user (User): The new user to register
    
    """
    hashed_password = hash_string(str(new_user.password.password))
    
    client = await get_postgres_client(database = USER_DATABASE)

    values_to_insert:dict = {
        "user": (new_user._id,
                    new_user.username,
                    hashed_password,
                    new_user._role,
                    new_user._verified,
                ),
        "info": (new_user._id,
                    None,
                    None,
                    None,
                    None,
                    None,
                    new_user.email,
                ),
        "log": (new_user._id,
                    new_user._created_at,
                    new_user._updated_at,
                    new_user._last_login,
                ),
        }

    try:
        await client.execute(query_insert_new_user, *values_to_insert["user"])
        await client.execute(query_insert_user_info, *values_to_insert["info"])
        await client.execute(query_insert_user_log, *values_to_insert["log"])
    
    except Exception as e:
        raise CustomException(name = "Register error",
                              error_code = 500,
                              message = f"Failed to register the user: {e}")
                              

    finally:
        await client.close()



async def update_user_password(user_who_updates:str, new_password:Password) -> None:
    """
    Update the user password in the database.

    Args:
        - user_who_updates (str): The username of the user who updates the password
        - new_password (Password): The new password to update
    
    Raises:
        - CustomException: If the password update fails
    """
    hashed_password = hash_string(new_password.password)
    query_args:tuple = (hashed_password, user_who_updates,)


    client = await get_postgres_client(database = USER_DATABASE)

    try:
        await client.execute(query_update_user_password, *query_args)
    except Exception as e:
        raise CustomException(name = "Password update error", 
                              error_code = 500,
                              message = f"Failed to update user password in the database: {e}")
    finally:
        await client.close()



async def update_user_last_login(username:str) -> None:
    """
    Update the last_login timestamp of the user in the database.

    Raises:
        - CustomException: If the last login update fails
    """
    client = await get_postgres_client(database = USER_DATABASE)

    try:
        await client.execute(query_update_user_last_login, username)
    except Exception as e:
        raise CustomException(name = "User last login error", 
                              error_code = 500,
                              message = f"Failed to update user last login date in the database: {e}")
    finally:
        await client.close()



async def get_carto_from_database(params_location:ParamsLocation) -> dict:
    """
    Return geographic data from the Postgres database (uses postgis) depending on the location and the data type requested.

    args:
        - params_location (ParamsLocation): The location parameters to get the data from the database
    
    raises:
        - CustomException: If the connection to the database fails

    returns:
        - A dictionary containing the data requested
    """
    try:
        client = await get_postgres_client(database = CARTO_DATABASE)


    except Exception as e:
        raise CustomException(name = "Error: Postgres connection",
                              error_code = 500,
                              message = f"Failed to connect to the Postgres database: {e}")


    else:
        data_type_to_request = params_location.data_type

        data_to_return = {}


        projection = get_projection(params_location.latitude, params_location.longitude)
        location_name = params_location.location_name.replace("'", "''")


        if "rpg" in data_type_to_request:
            for year in params_location.years:
                params = (params_location.latitude, params_location.longitude, params_location.radius, year, projection, location_name)
                
                response_data = await client.fetch(query_get_rpg_location, *params)
                
                data_to_return[f"rpg-{year}"] = {
                    f"rpg-{year}": [
                        {
                            **dict(record),  # Conversion en dictionnaire
                            "geometry": str(shapely.wkb.loads(record["geometry"]))#.__geo_interface__  # Conversion en format GeoJSON
                        } 
                        for record in response_data
                    ]
                }

        if "clc" in data_type_to_request:
            for year in params_location.years:
                params = (params_location.latitude, params_location.longitude, params_location.radius, year, projection, location_name)

                response_data = await client.fetch(query_get_clc_location, *params)

                data_to_return[f"clc-{year}"] = {
                    f"clc-{year}": [
                        {
                            **dict(record),  # Conversion en dictionnaire
                            "geometry": str(shapely.wkb.loads(record["geometry"]))  # Conversion en format GeoJSON
                        }
                        for record in response_data
                    ]
                }

        if "foret_v2" in data_type_to_request:
            # Voir instructions plus haut
            pass

            # for year in params_location.years:
            #     params = (params_location.latitude, params_location.longitude, params_location.radius, year, projection, location_name)

            #     response_data = await client.fetch(query_get_foretV2_location, *params)

            #     data_to_return[f"foret_v2-{year}"] = {
            #         f"foret_v2-{year}": [
            #             {
            #                 **dict(record),  # Conversion en dictionnaire
            #                 "geometry": str(shapely.wkb.loads(record["geometry"]))  # Conversion en format GeoJSON
            #             }
            #             for record in response_data
            #         ]
            #     }
        
        if "c1l" in data_type_to_request:

            # Voir instructions plus haut
            pass


        return data_to_return