#airflow/code/dags/cartographic_functions.py


# LIB
import numpy as np
import pandas as pd
import requests

from utils.logger import basic_logger


# CARTOGRAPHIC FUNCTIONS
def create_cartographic_aggregated_df(**kwargs) -> pd.DataFrame:
    """
    Aggregate the DataFrame by the groupby_cols and return the DataFrame with the groupby_cols only.

    args:
        - **kwargs: dict with the following keys
            - task_instance: task_instance object
            - task_ids: str, task id to pull the XCom
            - groupby_cols: list, columns to group by

    return:
        - pd.DataFrame: DataFrame with the groupby_cols only
    """
    task_instance = kwargs.get('task_instance')
    df = task_instance.xcom_pull(task_ids = kwargs["task_ids"])

    loc_gb = df.groupby(kwargs["groupby_cols"]).size().reset_index(name = "count")
    loc_gb.drop(columns = ["count"], inplace = True)

    basic_logger.info(f"Len df: {len(loc_gb)}")

    return loc_gb



def fetch_cartographic_data(**kwargs) -> pd.DataFrame:
    """
    Fetch the cartographic data from the API and fill the DataFrame with the culture and bio values.

    args:
        - **kwargs: dict with the following keys
            - task_instance: task_instance object
            - task_ids: str, task id to pull the XCom
            - url: str, url to fetch the data
            - radius: int, radius to fetch the data

    return:
        - pd.DataFrame: DataFrame with the culture and bio values
    """
    task_instance = kwargs.get('task_instance')
    df_to_fill = task_instance.xcom_pull(task_ids = kwargs["task_ids"])


    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }



    for index, row in df_to_fill.iterrows():
        data_to_request = [
            {
                "location_name": "location",
                "latitude": row["lat"],
                "longitude": row["lon"],
                "data_type": ["rpg"],
                "years": [2022],
                "radius": kwargs["radius"]
            }
        ]

        try:
            results = requests.post(kwargs["url"], headers = headers, json = data_to_request)
            results_json = results.json()

        except:
            basic_logger.error(f"Error: {results.text}")
            df_to_fill.loc[index, "culture"] = np.nan
            df_to_fill.loc[index, "bio"] = np.nan

        else:
            year = 2022
            basic_logger.info(f"Results: {results_json}")
            if results_json["location"][f"rpg-{year}"][f"rpg-{year}"]:
                culture = results_json["location"][f"rpg-{year}"][f"rpg-{year}"][0]["culture"]
                bio = results_json["location"][f"rpg-{year}"][f"rpg-{year}"][0]["bio"]
                legende = results_json["location"][f"rpg-{year}"][f"rpg-{year}"][0]["legende"]
                df_to_fill.loc[index, "culture"] = culture
                df_to_fill.loc[index, "bio"] = bio
                df_to_fill.loc[index, "legende"] = legende
            else:
                df_to_fill.loc[index, "culture"] = np.nan
                df_to_fill.loc[index, "bio"] = np.nan
                df_to_fill.loc[index, "legende"] = np.nan

    return df_to_fill