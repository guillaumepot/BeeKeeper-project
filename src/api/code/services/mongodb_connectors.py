# api/services/mongodb_connectors.py


# Lib
from motor.motor_asyncio import AsyncIOMotorClient

from models.user_objects_base_models import Locations
from models.user_objects_base_models import Hives
from utils.config import MONGODB_HOST, MONGODB_PORT, MONGODB_API_USER, MONGODB_API_PASSWORD, MONGODB_DATABASE, MONGODB_LOCATION_COLLECTION_NAME, MONGODB_HIVE_COLLECTION_NAME
from utils.exceptions import CustomException




async def get_mongodb_client() -> AsyncIOMotorClient:
    """
    Get a connection to the MongoDB database.

    Returns:
        - A connection to the MongoDB database (client)

    Raises:
        - CustomException if the connection fails
    """
    try:
        client = AsyncIOMotorClient(
            f"mongodb://{MONGODB_API_USER}:{MONGODB_API_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/admin"
        )


    except Exception as e:
        raise CustomException(
            name = "Error: MongoDB connection",
            error_code = 500,
            message = f"Failed to connect to the MongoDB database: {e}"
        )

    else:
        return client
    


async def get_collection(collection_name:str, database:str = MONGODB_DATABASE) -> AsyncIOMotorClient:
    """
    Get a collection from the MongoDB database.

    Args:
        - collection_name (str): The name of the collection to get

    Returns:
        - A collection from the MongoDB database

    Raises:
        - CustomException if the connection fails
    """
    try:
        client = await get_mongodb_client()
    except Exception as e:
        raise CustomException(
            name = "Error: MongoDB connection",
            error_code = 500,
            message = f"Failed to connect to the MongoDB database: {e}"
        )
    else:
        client_db = client[database]
        return client_db[collection_name]
    


async def request_user_locations(user_id: str = None, method: str = "GET", location: Locations = None) -> dict:
    """
    Request the user's locations from the MongoDB database.

    Args:
        - user_id (str): The user's ID
        - method (str): The method to use (GET, POST, PUT, DELETE)
        - location (Locations): The location object to use

    Returns:
        - A dictionary with the requested locations

    Raises:
        - CustomException if the connection fails
    """
    try:
        collection = await get_collection(MONGODB_LOCATION_COLLECTION_NAME)

    except Exception as e:
        raise CustomException(
            name = "Error: MongoDB collection",
            error_code = 500,
            message = f"Failed to get the collection from the MongoDB database: {e}"
        )
    
    else:
        if method == "GET":
            cursor = collection.find({"owner": user_id})
            document = await cursor.to_list(length=None)
            if document:
                for doc in document:
                    doc['_id'] = str(doc['_id'])
            return document if document else {}

        elif method == "POST":
            await collection.insert_one(location.dict())
            return {"status": "success", "message": "Location added", "location": location.dict()}

        elif method == "PUT":
            await collection.update_one({"owner": location.owner, "name": location.name}, {"$set": location.dict()})
            return {"status": "success", "message": "Location updated"}

        elif method == "DELETE":
            await collection.delete_one({"name": location.name, "latitude": location.latitude, "longitude": location.longitude})
            return {"status": "success", "message": "Location deleted"}

        else:
            raise CustomException(
            name = "Error: Wrong Method",
            error_code = 400,
            message = f"Wrong method used: {method}. Method must be GET, POST, PUT or DELETE"
        )


async def request_user_hives(user_id: str = None, method: str = "GET", hive: Hives = None) -> dict:
    """
    Request the user's hives from the MongoDB database.

    Args:
        - user_id (str): The user's ID
        - method (str): The method to use (GET, POST, PUT, DELETE)
        - location (Locations): The hive object to use

    Returns:
        - A dictionary with the requested hives

    Raises:
        - CustomException if the connection fails
    """
    try:
        collection = await get_collection(MONGODB_HIVE_COLLECTION_NAME)

    except Exception as e:
        raise CustomException(
            name = "Error: MongoDB collection",
            error_code = 500,
            message = f"Failed to get the collection from the MongoDB database: {e}"
        )
    
    else:
        if method == "GET":
            cursor = collection.find({"owner": user_id})
            document = await cursor.to_list(length=None)
            if document:
                for doc in document:
                    doc['_id'] = str(doc['_id'])
            return document if document else {}

        elif method == "POST":
            await collection.insert_one(hive.dict())
            return {"status": "success", "message": "Hive added", "hive": hive.dict()}

        elif method == "PUT":
            await collection.update_one({"owner": hive.owner, "name": hive.name}, {"$set": hive.dict()})
            return {"status": "success", "message": "Hive updated"}

        elif method == "DELETE":
            await collection.delete_one({"name": hive.name})
            return {"status": "success", "message": "Hive deleted"}

        else:
            raise CustomException(
            name = "Error: Wrong Method",
            error_code = 400,
            message = f"Wrong method used: {method}. Method must be GET, POST, PUT or DELETE"
        )