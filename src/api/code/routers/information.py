#api/routers/information.py


# Lib
from fastapi import APIRouter, Depends, Request

from services.auth import get_current_user
from services.mongodb_connectors import get_mongodb_client
from services.postgres_connectors import get_postgres_client
from services.redis_connectors import get_redis_client
from utils.config import CURRENT_VERSION, POSTGRES_HOST, POSTGRES_PORT, MONGODB_HOST, MONGODB_PORT
from utils.config import DATABASE_CHECK_LIMIT
from utils.decorators import require_role
from utils.exceptions import CustomException
from utils.limiter import limiter




"""
Router Declaration
"""
information = APIRouter()


"""
Routes Declaration
"""

@information.get(f"/", tags = ["info"])
def get_root_api():
    """
    Text displayed when accessing the root of the API (/)
    """
    text = (
        "Welcome to the API module of the BeeM project\n"
        "This API module is used to connect UI, Databases and other services\n"
        "To get started, please refer to the documentation on the following route: /docs\n"
        "You can also test the API using the following route: /test/hello\n"
        "For more information, please refer to the README file on the GitLab repository"
    )
    return text



@information.get(f"/{CURRENT_VERSION}/status", tags = ["info"])
def get_api_status(request: Request):
    """
    Get the status of the API
    Docker compose HEALTHCHECK is based on this route
    """
    return {"status": f"API is running, version: {CURRENT_VERSION}"}



@information.get(f"/{CURRENT_VERSION}/postgres/check", tags = ["info"])
@limiter.limit(DATABASE_CHECK_LIMIT)
@require_role(role = "admin")
async def check_postgres_availability(request: Request, JWT_TOKEN: dict = Depends(get_current_user)):
    """
    Check the connection to the PostgreSQL database using pg_isready
    """
    try:
        client = await get_postgres_client(database = "postgres")
        return {"status": "PostgreSQL is available", "host": POSTGRES_HOST, "port": POSTGRES_PORT}

    except Exception as e:
        raise CustomException(name = "postgres_unavailable",
                              error_code = 503,
                              message = "Caught an exception while checking PostgreSQL availability") from e




@information.get(f"/{CURRENT_VERSION}/mongodb/check", tags = ["info"])
@limiter.limit(DATABASE_CHECK_LIMIT)
@require_role(role = "admin")
async def check_mongodb_availability(request: Request, JWT_TOKEN: dict = Depends(get_current_user)):
    """
    Check the connection to the MongoDB database using pg_isready
    """
    try:
        client = await get_mongodb_client()
        await client.admin.command('ping')
        return {"status": "MongoDB is available", "host": MONGODB_HOST, "port": MONGODB_PORT}

    except Exception as e:
        raise CustomException(name = "mongodb_unavailable",
                              error_code = 503,
                              message = "Caught an exception while checking MongoDB availability") from e




@information.get(f"/{CURRENT_VERSION}/redis/check", tags = ["info"])
@limiter.limit(DATABASE_CHECK_LIMIT)
@require_role(role = "admin")
async def check_redis_availability(request: Request, JWT_TOKEN:dict = Depends(get_current_user)):
    """
    Check the connection to the Redis database using the JSON module
    """
    json_test_data = [{
        "name": "test data",
        "value": "Hello World!"
    }]

    try:
        client = await get_redis_client()
        client.json().set("test", "$", json_test_data)
        
        redis_read_data = client.json().get("test", "$", json_test_data)
        return {"From Redis:": redis_read_data}

    except Exception as e:
        raise CustomException(name = "redis_unavailable",
                              error_code = 503,
                              message = "Caught an exception while checking Redis availability") from e