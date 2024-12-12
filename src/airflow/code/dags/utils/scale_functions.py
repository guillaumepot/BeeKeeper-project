#airflow/code/dags/scale_functions.py



# LIB
from scipy.stats import zscore
import numpy as np
import pandas as pd
from typing import Callable



from utils.generic_functions import convert_dict_df
from utils.logger import basic_logger




"""
CLEANING SCALE FUNCTIONS
"""
def corr_zscore(x, quant_corr = 0.995):
    """
    Apply zscore method to remove anomalies from time weight series.
    x must be a time-ordered series of weight measured by one scale (and only one !).
    """
    
    diff = np.append(np.array(0), np.diff(x))
    zscore_x = zscore(diff)

    z_treshold = np.quantile(zscore_x, quant_corr)
    
    corr = x
    
    for idx in range(len(x)):
        if (abs(zscore_x[idx]) > z_treshold):
            corr[idx:] = (x[idx:] - diff[idx])
            
    return(corr)



def correct_weight_variations(df: pd.DataFrame, method:Callable = corr_zscore) -> pd.DataFrame:
    """
    Corrects weight variations in a DataFrame using a specified method.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing weight data. 
                        It must have columns "bal" for scale identifier and "poids" for weight values.
    method (Callable, optional): The method to use for correcting weight variations. 
                                    Defaults to corr_zscore.

    Returns:
    pd.DataFrame: The DataFrame with an additional column "corrected_weight" containing the corrected weight values.
    """
    for scale in df["bal"].unique():
        mask = df["bal"] == scale
        df.loc[mask, "corrected_weight"] = method(df.loc[mask, "poids"].values)

    return df




def clean_scale_data(weight_variation_function:Callable = correct_weight_variations, **kwargs) -> dict:
    """
    Cleans and processes scale data from a combined DataFrame, applies weight variation corrections, and returns the cleaned DataFrame.
    Args:
        weight_variation_function (Callable, optional): Function to correct weight variations. Defaults to correct_weight_variations.
        **kwargs: Additional keyword arguments required for processing:
            - task_instance: The task instance from which to pull XCom data.
            - task_ids: The task IDs to pull XCom data from.
            - weight_interval_min: Minimum acceptable weight value.
            - weight_interval_max: Maximum acceptable weight value.
            - min_date: Minimum acceptable date for the data.
    Returns:
        dict: The cleaned and processed DataFrame as a dictionary.
    Raises:
        ValueError: If the cleaned combined DataFrame is empty.
    Notes:
        - The function handles location data by correcting inverted latitude and longitude values for specific providers.
        - It removes rows with missing or zero latitude/longitude values.
        - It filters out rows with weight values outside the specified interval.
        - Unnecessary columns are dropped, and the DataFrame is cleaned of NaN values and duplicates.
        - Rows with dates before the specified minimum date are removed.
        - The DataFrame is sorted by time, and a new date column is added.
        - The weight variation function is applied to the cleaned DataFrame.
    """
    # FUNCTION LOGIC
    task_instance = kwargs.get('task_instance')
    combined_dict = task_instance.xcom_pull(task_ids = kwargs["task_ids"])

    combined_df = convert_dict_df(combined_dict) # Reverse previous conversion to DataFrame (dict -> DataFrame due to XCom serialization)
    basic_logger.info(f"Combined DataFrame: {combined_df.shape}")


    # CLEAN LOGIC
    # LOCATION (LAT / LON)
    # Some providers invert LAT & LON
    if (combined_df['const'] == 'LAB').any():
        combined_df['lat'], combined_df['lon'] = combined_df['lon'], combined_df['lat']

    # Remove missing lat/long values
    combined_df = combined_df.dropna(subset=['lat', 'lon'])
    combined_df = combined_df[(combined_df['lat'] != 0) & (combined_df['lon'] != 0)]

    # WEIGHTS
    # Remove bad weight values (not in the weight_interval)
    combined_df = combined_df[(combined_df['poids'] > kwargs["weight_interval_min"]) & (combined_df['poids'] < kwargs["weight_interval_max"])]

    # COLS
    # Remove unnecessary columns (keep const for weight variation), drop NaN et duplicates
    combined_df = combined_df.drop(columns=['name', 'ruche', 'qloc', 'activ'])
    combined_df = combined_df.dropna()
    combined_df.drop_duplicates(inplace=True)

    # Dates before specified min date are not kept
    combined_df = combined_df[combined_df['time'] > kwargs["min_date"]]
    
    # Sort by time col & reset index
    combined_df = combined_df.sort_values(by=['time'])
    combined_df.reset_index(drop=True, inplace=True)
    # Add a date col containing the date extracted from the time col
    combined_df['date'] = pd.to_datetime(combined_df['time']).dt.date
    combined_df['date'] = combined_df['date'].astype(str)

    # END OF CLEAN LOGIC


    # WEIGHT VARIATION LOGIC
    corrected_combined_df = weight_variation_function(combined_df)

    # END OF WEIGHT VARIATION LOGIC



    if corrected_combined_df.empty:
        basic_logger.warning("Cleaned combined DataFrame is empty, failing task...")
        raise ValueError("Cleaned combined DataFrame is empty")
    
    return corrected_combined_df
