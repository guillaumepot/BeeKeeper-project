#airflow/code/dags/functions.py



# LIB
import numpy as np
from openmeteo_requests.Client import OpenMeteoRequestsError
import pandas as pd

from utils.config import openmeteo, historical_forecast_url, params_daily_weather, openmeteo_models
from utils.logger import basic_logger




"""
WEATHER REQUEST FUNCTIONS
"""
def get_start_end_date_by_location(**kwargs) -> pd.DataFrame:
    """
    Prepare a DataFrame with the first and last date for each location to be used in the next task (request weather data)

    args:
        - task_ids (str): task ID to pull the data from

    returns:
        - pd.DataFrame: DataFrame with the first and last date for each location
    """
    task_instance = kwargs.get('task_instance')
    df_to_fill = task_instance.xcom_pull(task_ids = kwargs["task_ids"])

    # Group by location and date to get the first and last date for each location
    weather_agg_df = df_to_fill.groupby(["lat", "lon", "date"]).size().reset_index(name = "count")
    weather_agg_df.drop(columns = ["count"], inplace = True)
    # Get the first and last date for each location and return it

    weather_agg_df = weather_agg_df.groupby(['lat', 'lon']).agg(date_min = ('date', 'min'), date_max = ('date', 'max')).reset_index()
    basic_logger.info(f"Len weather_agg_df: {len(weather_agg_df)}")

    return weather_agg_df




def transform_and_return_openmeteoapi_response(parameters:dict) -> dict:
    """
    Request openmeteo data et transform the response to a dictionary

    args:
        - parameters (dict): Parameters to be used in the request

    returns:
        - dict: Dictionary with the response from OpenMeteo API
    """
    
    def request_openmeteo(parameters:dict) -> dict:
        """
        Request OpenMeteo API and return the response

        args:
            - parameters (dict): Parameters to be used in the request

        returns:
            - dict: Response from Open
        
        """

        responses = openmeteo.weather_api(historical_forecast_url, params = parameters)
        response = responses[0]

        return response


    response = request_openmeteo(parameters)

    daily = response.Daily()

    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}


    for index, elt in enumerate(params_daily_weather):
        daily_data[elt] = daily.Variables(index).ValuesAsNumpy()


    for key, value in daily_data.items():
        if isinstance(value, list) or isinstance(value, int):
            pass
        else:
            daily_data[key] = value.tolist()

    return daily_data





def fetch_weather_data(**kwargs) -> pd.DataFrame:
    """
    Fetches weather data for given locations and dates, processes the data, and returns it as a DataFrame.

    Args:
        **kwargs: Arbitrary keyword arguments. Expected keys include:
            - task_instance: The task instance object from which to pull data using XCom.
            - task_ids: The task ID to pull data from.

    Returns:
        pd.DataFrame: A DataFrame containing the weather data for the specified locations and dates.

    Raises:
        OpenMeteoRequestsError: If there is an error fetching data from the OpenMeteo API.

    Notes:
        - The function expects the DataFrame pulled from XCom to have columns 'lat', 'lon', 'date_min', and 'date_max'.
        - In case of an error fetching data for a location, the function logs the error and fills the data with NaNs for that location.
    """
    task_instance = kwargs.get('task_instance')
    df_with_loc_and_date = task_instance.xcom_pull(task_ids = kwargs["task_ids"])


    no_data_loc_list : list = []
    results = []

    for index, row in df_with_loc_and_date.iterrows():

        params = {
            "latitude": row["lat"],
            "longitude": row["lon"],
            "daily": params_daily_weather,
            "models": openmeteo_models,
            "start_date": row["date_min"],
            "end_date": row["date_max"]
        }


        try:
            weather_data = transform_and_return_openmeteoapi_response(params)

        except OpenMeteoRequestsError as e:
            basic_logger.error(f"Error for location ({row["lat"]}, {row["lon"]}): {e}")
            no_data_loc_list.append((row["lat"], row["lon"]))
            weather_data = {key: np.nan for key in params_daily_weather}
            print(weather_data)
        finally:
            weather_data["date"] = [x.strftime('%Y-%m-%d') for x in weather_data["date"]]
            weather_data["lat"] = row["lat"]
            weather_data["lon"] = row["lon"]
            results.append(pd.DataFrame(weather_data))

    output_df = pd.concat(results, ignore_index=True)

    return output_df