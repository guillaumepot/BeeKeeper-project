#airflow/code/dags/generic_functions.py



# LIB
from airflow.models import XCom
from airflow.utils.db import provide_session
import os
import pandas as pd
from typing import Union


from utils.logger import basic_logger




"""
GENERAL FUNCTIONS
"""
@provide_session
def cleanup_xcom(session=None):
    """
    Function to cleanup all XComs from the Airflow database.
    """
    session.query(XCom).delete()
    session.commit()



def convert_dict_df(data_object:Union[dict, pd.DataFrame] = None) -> Union[pd.DataFrame, dict]:
    """
    Convert a dict to a DataFrame or a DataFrame to a dict depending on the output parameter

    args:
        data_object (Union[dict, pd.DataFrame]): data object to convert
    return:
        Union[pd.DataFrame, dict]: converted data object
    raises: 
        ValueError: if data_object is None or empty
    """
    if data_object is None:
        raise ValueError("data_object is None")
    
    if isinstance(data_object, dict):
        if len(data_object) == 0:
            raise ValueError("dict is empty")
        else:
            return pd.DataFrame(data_object)
        

    elif isinstance(data_object, pd.DataFrame):
        if data_object is None or data_object.empty:
            raise ValueError("df is empty")
        else:
            return data_object.to_dict()



def save_df_to_file(**kwargs) -> None:
    """
    Save DataFrame to a parquet file in the specified directory

    args:
    - task_ids: str - Ids of the task returning the DataFrame
    - filename: str - Name of the file to save
    - savedir: str - Directory to save the file
    - prefix: str - prefix to add to the file name (default: None)
    """
    task_instance = kwargs.get('task_instance')
    df = task_instance.xcom_pull(task_ids = kwargs["task_ids"])

    if kwargs["prefix"] is None:
        filepath = kwargs["savedir"] + "/" + kwargs["filename"] + ".parquet"
    else:
        filepath = kwargs["savedir"] + "/" + kwargs["prefix"] + "_" + kwargs["filename"] + ".parquet"

    df.to_parquet(filepath, index=False)

    basic_logger.info(f"Data saved to {filepath}")



def create_aggregated_df(**kwargs) -> None:
    """
    Create an aggregated DataFrame from a DataFrame and save it to a file

    args:
        df (pd.DataFrame): input DataFrame
        groupby_cols (Union[str, list]): columns to group by
        agg_cols (Union[str, list]): columns to aggregate
        agg_funcs (Union[str, list]): aggregation functions
    """
    if isinstance(kwargs["groupby_cols"], str):
        groupby_cols = [kwargs["groupby_cols"]]
    else:
        groupby_cols = kwargs["groupby_cols"]
    if isinstance(kwargs["agg_cols"], str):
        agg_cols = [kwargs["agg_cols"]]
    else:
        agg_cols = kwargs["agg_cols"]
    if isinstance(kwargs["agg_funcs"], str):
        agg_funcs = [kwargs["agg_funcs"]]
    else:
        agg_funcs = kwargs["agg_funcs"]

    df = load_file_as_dataframe(kwargs["filepath"])

    agg_df = df.groupby(groupby_cols)[agg_cols].agg(agg_funcs).reset_index()


    if kwargs["rename_cols"] == True:
        agg_df.columns = kwargs["new_col_names"]
    if kwargs["col_to_keep"]:
        agg_df.drop(columns = [col for col in agg_df.columns if col not in kwargs["col_to_keep"]], inplace = True)

    return agg_df
    



def load_file_as_dataframe(path:str) -> pd.DataFrame:
    """
    Load a file into a pandas DataFrame based on the file extension

    args:
    - filepath: str - File to load

    returns:
    - pd.DataFrame: DataFrame of the file

    raises:
    - Exception: If the file extension is not supported or the file cannot be loaded

    """
    basic_logger.info(f"Loading: {path}")
    extension = os.path.splitext(path)[1]


    try:
        if extension == ".csv" or extension == ".txt":
            df = pd.read_csv(path)
        elif extension == ".xlsx":
            df = pd.read_excel(path)
        elif extension == ".json":
            df = pd.read_json(path)
        elif extension == ".parquet":
            df = pd.read_parquet(path)

        basic_logger.info(f"Loaded: {path}")

    except Exception as e:
        raise e
    
    else:
        return df




def load_and_combine_dataframes(dirpath:str) -> dict:
    """
    Load and combine all files in a directory into a single DataFrame

    args:
        - path: str - Directory path to load files from

    returns:
        - dict: Combined DataFrame as a dictionary

    raises:
        - ValueError: If the combined DataFrame is empty
        - Exception: If there is an error loading a file
    """

    combined_df = pd.DataFrame()

    for file in os.listdir(dirpath):
        filepath = os.path.join(dirpath, file)

        try:
            df = load_file_as_dataframe(filepath)
        except Exception as e:
            basic_logger.warning(f"Error loading file: {filepath}")
            basic_logger.warning(e)


        else:
            combined_df = pd.concat([combined_df, df])

        finally:  
            basic_logger.info(f"Combined DataFrame: {combined_df.shape}")


    if combined_df.empty:
        basic_logger.warning("Combined DataFrame is empty, exiting task...")
        raise ValueError("Combined DataFrame is empty")

    else:
        combined_dict = convert_dict_df(combined_df)  # Convert to dict avoids issues with XCom serialization
        return combined_dict



def join_dataframes(**kwargs) -> pd.DataFrame:
    """
    Join two DataFrames on specified columns

    args:
        df1 (pd.DataFrame): first DataFrame
        df2 (pd.DataFrame): second DataFrame
        on_cols (Union[str, list]): columns to join on
        how (str): type of join

    return:
        joined_df (pd.DataFrame): joined DataFrame
    """
    task_instance = kwargs.get('task_instance')
    df1 = task_instance.xcom_pull(task_ids = kwargs["task_ids1"])
    df2 = task_instance.xcom_pull(task_ids = kwargs["task_ids2"])
    basic_logger.info(f"DataFrames loaded: {df1.shape}, {df2.shape}")

    cols_joined = kwargs["on_cols"]

    joined_df = pd.merge(df1, df2, on = cols_joined, how = kwargs["how"])

    return joined_df



def fillna_dataframe(**kwargs) -> pd.DataFrame:
    """
    
    """
    task_instance = kwargs.get('task_instance')
    df = task_instance.xcom_pull(task_ids = kwargs["task_ids"])
    df.fillna(kwargs["default_value"], inplace = True)
    

    return df