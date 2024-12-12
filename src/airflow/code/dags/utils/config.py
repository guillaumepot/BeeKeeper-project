#airflow/code/dags/config.py

# Lib
import os
import openmeteo_requests
import requests_cache
from retry_requests import retry



# Dag Schedulers
ETL_PIPELINE_SCHEDULER = os.getenv("ETL_PIPELINE_SCHEDULER")

# By default these dags are set to None and triggered by ETL PIPELINE DAG
SEGMENTED_PIPELINE_SCHEDULER = os.getenv("SEGMENTED_PIPELINE_SCHEDULER")
ML_PIPELINE_SCHEDULER = os.getenv("ML_PIPELINE_SCHEDULER")



# Storage directories
STORAGE_DIR = "/opt/airflow/storage"
RAW_DATA_DIR = f"{STORAGE_DIR}/raw_data"
PROCESSING_DATA_DIR = f"{STORAGE_DIR}/processing_data"
CLEANED_DATA_DIR = f"{STORAGE_DIR}/cleaned_data"
ARCHIVES_DATA_DIR = f"{STORAGE_DIR}/archives_data"
SEGMENTATION_MODEL_DIR = f"{STORAGE_DIR}/segmentation_models"
MLFLOW_TRACKING_URI = "/opt/airflow/storage/mlflow/"



# Setup OpenMeteo API
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

historical_forecast_url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
openmeteo_models = ["best_match"]
params_daily_weather = ["weather_code", "temperature_2m_max", "temperature_2m_min", "sunrise", "sunset", "uv_index_max", "precipitation_sum", "rain_sum", "showers_sum", "snowfall_sum", "wind_speed_10m_max", "wind_direction_10m_dominant"]



# API Variables
API_URL = os.getenv("API_URL")
API_VERSION = os.getenv("API_VERSION")
ROUTE_CARTO_SUFIX = os.getenv("ROUTE_CARTO_SUFIX")
API_ROUTE_CARTO_URL = f"{API_URL}/{API_VERSION}/{ROUTE_CARTO_SUFIX}"
CARTO_DATA_RADIUS_REQUEST = 500



# MISC CONFIG (DAGs)
# File patterns
TEXT_FILE_PATTERN = "*.txt"
PARQUET_FILE_PATTERN = "*.parquet"
SEGMENTED_FILE_PATTERN = "segmented_*.parquet"

# ETL DAG
WEIGHT_INTERVAL_MIN:int = 15000
WEIGHT_INTERVAL_MAX:int = 200000
CLEAN_SCALE_MIN_DATE_TO_KEEP = "2022-01-01"

# SEGMENTATION DAG
SEGMENTATION_MIN_MONTH = "-04-01"
SEGMENTATION_MAX_MONTH = "-09-01"


# DATA ML PREPROCESSING
DF_FILLNA_DEFAULT_VALUE = 0
TARGET_COMLUMN = "Slope"
COLUMNS_TO_ENCODE = "scale"
OTHER_COL_TO_DROP = ["End", "Segment", "Slope", 
                     "Weight Start", "Weight End", "Weight diff",
                     "N", "NE", "E", "SE",
                     "S", "SW", "W", "NW"]


# MACHINE LEARNING MODELS
ML_MODEL_CHOICE = ("RandomForestRegressor", "LinearRegression", "SVR")


RFR_PARAMS = {
    "n_estimators": [50, 100, 200, 300, 500],
    "max_depth": [None, 5, 10, 15],
    "min_samples_split": [2, 4, 6],
    "criterion": ["friedman_mse", "squared_error"],
    "max_features": ["auto", "sqrt", "log2"]
}

SVR_PARAMS = {
    "kernel": ["linear", "rbf"],
    "C": [0.1, 1, 10],
    "gamma": ["scale", "auto"]
}

LR_PARAMS = {
    "fit_intercept": [True, False]
}


MODEL_TEST_PARAMS = (RFR_PARAMS, LR_PARAMS, SVR_PARAMS)