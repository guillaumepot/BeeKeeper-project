# api/services/redis_connectors.py


# Lib
import redis


from utils.config import REDIS_HOST, REDIS_PORT
from utils.exceptions import CustomException



async def get_redis_client() -> redis.Redis:
    """
    Get a connection to the Redis database.

    Returns:
        - A connection to the Redis database (client)

    Raises:
        - CustomException if the connection fails
    """
    try:
        client = redis.Redis(host = REDIS_HOST,
                             port = REDIS_PORT,
                             decode_responses = False,
                            #  username = REDIS_API_USER,
                            #  password = REDIS_API_PASSWORD
                             )

    except Exception as e:
        raise CustomException(
            name = "Error: Redis connection",
            error_code = 500,
            message = f"Failed to connect to the Redis database: {e}"
        )

    else:
        return client