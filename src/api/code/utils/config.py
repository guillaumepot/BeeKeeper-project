#api/utils/config.py

import os
from passlib.context import CryptContext



# -----------------------------------------------------------------------------------------------------#


"""
General configuration
"""
# Influence the API behavior
DEBUG = os.getenv("DEBUG", False)
LOGGER = os.getenv("LOGGER", False)
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH")


# API informations
CURRENT_VERSION = os.getenv("API_VERSION", "v0")


"""
Algorithms, security, secrets
"""
# Critical services, authentification
HASH_ALGORITHM = os.getenv("HASH_ALGORITHM", "bcrypt")
ENCODING_ALGORITHM = os.getenv("ENCODING_ALGORITHM", "HS256")
if os.path.exists('/run/secrets/JWT_secret_key'):
    with open('/run/secrets/JWT_secret_key', 'r') as file:
        JWT_SECRET_KEY = file.read().strip()
else:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret_key")


ACCESS_TOKEN_EXPIRATION_IN_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRATION_IN_MINUTES", 60))


# PWD CONTEXT (Passlib, Hash Algorithm)
PWD_CONTEXT = CryptContext(schemes=[HASH_ALGORITHM], deprecated="auto")


# -----------------------------------------------------------------------------------------------------#

"""
DATABASES
"""
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_API_USER = os.getenv("POSTGRES_API_USER")
if os.path.exists('/run/secrets/postgres_api_password'):
    with open('/run/secrets/postgres_api_password', 'r') as file:
        POSTGRES_API_PASSWORD = file.read().strip()
else:
    POSTGRES_API_PASSWORD = os.getenv("POSTGRES_API_PASSWORD", "postgres")

USER_DATABASE = os.getenv("USER_DATABASE")
CARTO_DATABASE = os.getenv("CARTO_DATABASE")


MONGODB_HOST = os.getenv("MONGODB_HOST")
MONGODB_PORT = os.getenv("MONGODB_PORT")
MONGODB_API_USER = os.getenv("MONGODB_API_USER")
if os.path.exists('/run/secrets/mongodb_api_password'):
    with open('/run/secrets/mongodb_api_password', 'r') as file:
        MONGODB_API_PASSWORD = file.read().strip()
else:
    MONGODB_API_PASSWORD = os.getenv("MONGODB_API_PASSWORD", "mongodb")



MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")
MONGODB_LOCATION_COLLECTION_NAME = os.getenv("MONGODB_LOCATION_COLLECTION_NAME")
MONGODB_HIVE_COLLECTION_NAME = os.getenv("MONGODB_HIVE_COLLECTION_NAME")


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
# REDIS_API_USER = os.getenv("REDIS_API_USER")              # Not used (Redis open connetions but private network)
# REDIS_API_PASSWORD = os.getenv("REDIS_API_PASSWORD")      # Not used (Redis open connetions but private network)



# -----------------------------------------------------------------------------------------------------#

"""
LIMITER SERVICE - BASE LIMITS
"""
# LIMITER SERVICE
LIMITER_TYPE = os.getenv("LIMITER_TYPE") # "ip" or "user_id"
DEFAULT_LIMITS_FOR_LIMITER = os.getenv("DEFAULT_LIMITS_FOR_LIMITER")


## ROUTER AUTHENTICATOR
###

## ROUTER INFORMATION
STATUS_LIMIT = os.getenv("STATUS_LIMIT")
DATABASE_CHECK_LIMIT = os.getenv("DATABASE_CHECK_LIMIT")


## ROUTER TESTER
TEST_LIMIT = os.getenv("TEST_LIMIT")

## ROUTER USER
INSERT_INFOS_LIMIT = os.getenv("INSERT_INFOS_LIMIT")
UPDATE_INFOS_LIMIT = os.getenv("UPDATE_INFOS_LIMIT")
PASSWORD_UPDATE_LIMIT = os.getenv("PASSWORD_UPDATE_LIMIT")
USER_LOCATIONS_LIMIT = os.getenv("USER_LOCATIONS_LIMIT")
USER_HIVES_LIMIT = os.getenv("USER_HIVES_LIMIT")

## ROUTER WEATHER
WEATHER_LIMIT = os.getenv("WEATHER_LIMIT")

## ROUTER CARTOGRAPHIC
CARTO_LIMIT = os.getenv("CARTO_LIMIT")


# -----------------------------------------------------------------------------------------------------#


"""
OPENMETEO API
"""
forecast_url = "https://api.open-meteo.com/v1/forecast"
historical_forecast_url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
openmeteo_models = ["meteofrance_arpege_europe", "meteofrance_arome_france"]
params_current_weather = ["temperature_2m", "relative_humidity_2m", "precipitation", "rain", "showers", "cloud_cover", "wind_speed_10m", "wind_direction_10m"]
params_daily_weather = ["temperature_2m_max", "temperature_2m_min", "sunrise", "sunset", "precipitation_sum", "rain_sum", "showers_sum"]
params_hourly_weather = ["temperature_2m", "relative_humidity_2m", "precipitation_probability", "rain", "showers", "snowfall", "weather_code", "surface_pressure", "cloud_cover_low", "cloud_cover_mid", "wind_speed_10m", "wind_direction_10m", "soil_temperature_6cm", "soil_temperature_18cm"]



# -----------------------------------------------------------------------------------------------------#

"""
CARTOGRAPHIC DATA TYPES
"""
AVAILABLE_DATA_TYPES = os.getenv("AVAILABLE_CARTO_DATA_TYPES", "rpg, clc").split(",")

