#airflow/code/dags/ETL_dag.py

"""
ETL DAG - Execute ETL pipeline to process raw providers scale data to cleaned data

Steps:
1. Detect new files in raw data directory
2. Load raw data into staging table
3. Clean data
4. Add weather data
5. Add cartographic data
6. Save cleaned data to final table
"""

# LIB
from airflow import DAG
from airflow.utils.dates import days_ago

import datetime


from utils.callbacks import alert_on_failure
from utils.config import ETL_PIPELINE_SCHEDULER as DAG_SCHEDULER
from utils.config import RAW_DATA_DIR, PROCESSING_DATA_DIR, CLEANED_DATA_DIR, ARCHIVES_DATA_DIR, TEXT_FILE_PATTERN
from utils.config import WEIGHT_INTERVAL_MIN, WEIGHT_INTERVAL_MAX, CLEAN_SCALE_MIN_DATE_TO_KEEP
from utils.config import API_ROUTE_CARTO_URL, CARTO_DATA_RADIUS_REQUEST
from utils.operators import generate_task_file_sensor, generate_task_python_operator, generate_task_bash_operator, generate_task_trigger_dag_operator



# Generic functions
from utils.generic_functions import load_file_as_dataframe, load_and_combine_dataframes, save_df_to_file, cleanup_xcom, create_aggregated_df, join_dataframes
# Scales functions
from utils.scale_functions import clean_scale_data
# Weather data functions
from utils.weather_functions import get_start_end_date_by_location, fetch_weather_data
# Cartographic functions
from utils.cartographic_functions import create_cartographic_aggregated_df, fetch_cartographic_data




"""
DAG Declaration
"""
dag_scale_etl_pipeline = DAG(
    dag_id = "scale_etl_pipeline",
    description = "ETL pipeline for processing raw providers scale data to cleaned data",
    tags = ["ETL", "data"],
    catchup = False,
    schedule_interval =  DAG_SCHEDULER,
    start_date = days_ago(1),
    doc_md = """
        ETL DAG - Execute ETL pipeline to process raw providers scale data to cleaned data

        Steps:
        1. Detect new files in raw data directory
        2. Load raw data into staging table
        3. Clean data
        4. Add weather data
        5. Add cartographic data
        6. Save cleaned data to final table
    """
)



"""
TASKS
"""


"""
BLOCK 1 - EXTRACT AND CLEAN SCALE DATA
"""
raw_file_sensor = generate_task_file_sensor(dag = dag_scale_etl_pipeline,
                                            task_id = f"Detect.Raw.Files",
                                            filepath = f"{RAW_DATA_DIR}/{TEXT_FILE_PATTERN}",
                                            poke_interval = 10,
                                            timeout = 30,
                                            doc_md = """
                                                Detect new files in raw data directory.
                                                - Succeed if new files are detected and continues the pipeline
                                                - Fail if no new files are detected after the timeout period

                                                Doesn't require any callback function.
                                                """
                                            )



raw_file_loader = generate_task_python_operator(dag = dag_scale_etl_pipeline,
                                            task_id = f"Load.Combine.Raw.Files",
                                            python_callable = load_and_combine_dataframes,
                                            op_kwargs = {"dirpath": RAW_DATA_DIR},
                                            retries = 3,
                                            retry_delay = datetime.timedelta(seconds = 10),
                                            trigger_rule = "all_success",
                                            on_failure_callback = alert_on_failure,
                                            doc_md = """
                                                Load and combine raw data files provided by scale partners into a single combined DataFrame
                                                - Suceed if the data is loaded and combined successfully
                                                - Fail if the data loading and combining process fails or if the dataframe is empty

                                                Triggers a callback on failure after 3 retries with a 10 second delay.
                                                """
                                            )



scale_data_cleaner = generate_task_python_operator(dag = dag_scale_etl_pipeline,
                                                   task_id = "Clean.Scale.Data",
                                                   python_callable = clean_scale_data,
                                                   op_kwargs = {"task_ids": "Load.Combine.Raw.Files",
                                                                "weight_interval_min": WEIGHT_INTERVAL_MIN,
                                                                "weight_interval_max": WEIGHT_INTERVAL_MAX,
                                                                "min_date": CLEAN_SCALE_MIN_DATE_TO_KEEP,
                                                                "processing_path": PROCESSING_DATA_DIR
                                                                },
                                                   retries = 0,
                                                   trigger_rule = "all_success",
                                                   on_failure_callback = alert_on_failure,
                                                   doc_md = """
                                                        Clean scale data by removing outliers and invalid data
                                                        - Succeed if the data is cleaned succesfully
                                                        - Fail if the data cleaning process fails or if the resulting dataframe is empty

                                                        Triggers a callback on failure.
                                                        """
                                                   )



save_cleaned_scale_data = generate_task_python_operator(dag = dag_scale_etl_pipeline,
                                                        task_id = "Save.Cleaned.Scale.Data",
                                                        python_callable = save_df_to_file,
                                                        op_kwargs = {"task_ids": "Clean.Scale.Data",
                                                                     "savedir": PROCESSING_DATA_DIR,
                                                                     "prefix": "cleaned",
                                                                     "filename": "scale_data"
                                                                     },
                                                        retries = 0,
                                                        trigger_rule = "all_success",
                                                        doc_md = """
                                                                Save cleaned scale data to a parquet file in the processing dir, ending block 1 tasks
                                                                """
                                                        )



move_raw_files_to_archives = generate_task_bash_operator(dag = dag_scale_etl_pipeline,
                                                        task_id = "Move.Raw.Files.To.Archives",
                                                        bash_command = f"""
                                                                mkdir -p {ARCHIVES_DATA_DIR}/{datetime.datetime.now().strftime("%Y-%m-%d")}
                                                                mv {RAW_DATA_DIR}/* {ARCHIVES_DATA_DIR}/{datetime.datetime.now().strftime("%Y-%m-%d")}
                                                                """,
                                                        retries = 0,
                                                        trigger_rule = "all_success",
                                                        doc_md = """
                                                                Move raw data files to archives when scale processing is complete
                                                                """
                                                        )



remove_xcom_block_1 = generate_task_python_operator(dag = dag_scale_etl_pipeline,
                                                    task_id = "Remove.Xcom.Block_1",
                                                    python_callable = cleanup_xcom,
                                                    retries = 0,
                                                    trigger_rule = "all_done",
                                                    doc_md = """
                                                        Clean up Xcom data
                                                        """
                                                    )


"""
BLOCK 2 - RELOAD CLEANED DATA, AGGREGATE, FETCH DATA AND SAVE
"""
scale_processing_file_loader_block2 = generate_task_python_operator(dag = dag_scale_etl_pipeline,
                                                                    task_id = f"Load.Cleaned.Scale.Data",
                                                                    python_callable = load_file_as_dataframe,
                                                                    op_kwargs = {"path": f"{PROCESSING_DATA_DIR}/cleaned_scale_data.parquet"},
                                                                    retries = 3,
                                                                    retry_delay = datetime.timedelta(seconds = 10),
                                                                    trigger_rule = "all_success",
                                                                    on_failure_callback = alert_on_failure,
                                                                    doc_md = """
                                                                            Load the cleaned scale data parquet file into a DataFrame to continue processing
                                                                                - Succeed if the file is loaded and the DataFrame is not empty
                                                                                - Fail if the file cannot be loaded or the DataFrame is empty
                                                                        """
                                                                    )


generate_aggregated_scale_data = generate_task_python_operator(dag = dag_scale_etl_pipeline,
                                                               task_id = "AggregatedScale.Data",
                                                               python_callable = create_aggregated_df,
                                                               op_kwargs = {"task_ids": "Load.Cleaned.Scale.Data",
                                                                            "filepath": f"{PROCESSING_DATA_DIR}/cleaned_scale_data.parquet",
                                                                            "groupby_cols": ["date", "const", "bal", "lat", "lon"],
                                                                            "agg_cols": ["poids", "corrected_weight"],
                                                                            "agg_funcs": ["mean", "median", "min", "max", "sum"],
                                                                            "rename_cols": True,
                                                                            "new_col_names": ['date','const','bal',
                                                                                              'lat','lon','poids_mean',
                                                                                              'poids_median','poids_min','poids_max',
                                                                                              'poids_sum','weight_variation_corrected_mean',
                                                                                              'weight_variation_corrected_median',
                                                                                              'weight_variation_corrected_min',
                                                                                              'weight_variation_corrected_max',
                                                                                              'weight_variation_corrected_sum'],
                                                                            "col_to_keep": ['date','const','bal',
                                                                                            'lat','lon','poids_mean',
                                                                                            'poids_median','poids_min',
                                                                                            'poids_max','weight_variation_corrected_sum'],
                                                                            },
                                                               retries = 0,
                                                               trigger_rule = "all_success",
                                                               doc_md = """
                                                                    Create aggregated scale data and save it in the processing directory
                                                                    """
                                                         )



remove_xcom_block_2 = generate_task_python_operator(dag = dag_scale_etl_pipeline,
                                                    task_id = "Remove.Xcom.Block_2",
                                                    python_callable = cleanup_xcom,
                                                    retries = 0,
                                                    trigger_rule = "all_done",
                                                    doc_md = """
                                                        Clean up Xcom data
                                                        """
                                                    )




"""
BLOCK 2a - ADD WEATHER DATA
"""
prepare_data_to_request_weather_data = generate_task_python_operator(dag = dag_scale_etl_pipeline,
                                                                    task_id = f"Weather.Data.Preparation",
                                                                    python_callable = get_start_end_date_by_location,
                                                                    op_kwargs = {"task_ids": "AggregatedScale.Data"},
                                                                    retries = 0,
                                                                    trigger_rule = "all_success",
                                                                    doc_md = """
                                                                        Prepare data to request weather data from OpenMeteo API (aggregate data based on location and dates)   
                                                                        Returns a DataFrame with the first and last date for each location as Xcom data
                                                                        """
                                                                    )



fetch_and_fill_weather_data = generate_task_python_operator(dag = dag_scale_etl_pipeline,
                                                            task_id = f"Fetch.Weather.Data",
                                                            python_callable = fetch_weather_data,
                                                            op_kwargs = {"task_ids": "Weather.Data.Preparation"},
                                                            retries = 3,
                                                            retry_delay = datetime.timedelta(seconds = 60),
                                                            on_failure_callback = alert_on_failure,
                                                            trigger_rule = "all_success",
                                                            doc_md = """
                                                                Use the prepared data to request weather data from OpenMeteo API and fill the aggregated scale data
                                                                    - Succeed if the weather data is fetched and filled in the aggregated scale data
                                                                    - Fail if the weather data cannot be fetched or filled in the aggregated scale data

                                                                Triggers a callback on failure after 3 retries with a 60 second delay.
                                                                """
                                                            )



save_fetched_weather_data = generate_task_python_operator(dag = dag_scale_etl_pipeline,
                                                        task_id = "Save.Fetched.Weather.Data",
                                                        python_callable = save_df_to_file,
                                                        op_kwargs = {"task_ids": "Fetch.Weather.Data",
                                                                     "savedir": PROCESSING_DATA_DIR,
                                                                     "prefix": "weather",
                                                                     "filename": "aggregated_data"
                                                                     },
                                                        retries = 0,
                                                        trigger_rule = "all_success",
                                                        doc_md = """
                                                                Save weather aggregated data to a parquet file in the processing dir, ending block 2a tasks
                                                                """
                                                        )


"""
BLOCK 2b - ADD CARTOGRAPHIC DATA
"""
prepare_aggregated_cartographic_data = generate_task_python_operator(dag = dag_scale_etl_pipeline,
                                                               task_id = "Cartographic.Data.Preparation",
                                                               python_callable = create_cartographic_aggregated_df,
                                                               op_kwargs = {"task_ids": "AggregatedScale.Data",
                                                                            "filepath": f"{PROCESSING_DATA_DIR}/cleaned_scale_data.parquet",
                                                                            "groupby_cols": ["lat", "lon"],
                                                                            },
                                                               retries = 0,
                                                               trigger_rule = "all_success",
                                                               on_failure_callback = alert_on_failure,
                                                               doc_md = """
                                                                    Prepare data to request cartographic data from our database through the  API (aggregate data based on location)   
                                                                    Returns a DataFrame with the different locations as Xcom data
                                                                    """
                                                         )


request_cartographic_data = generate_task_python_operator(dag = dag_scale_etl_pipeline,
                                                   task_id = "Fetch.Cartographic.Data",
                                                   python_callable = fetch_cartographic_data,
                                                   op_kwargs = {"task_ids": "Cartographic.Data.Preparation",
                                                                "url": API_ROUTE_CARTO_URL,
                                                                "radius": CARTO_DATA_RADIUS_REQUEST,
                                                                },  
                                                   retries = 3,
                                                   retry_delay = datetime.timedelta(seconds = 180),
                                                   trigger_rule = "all_success",
                                                   on_failure_callback = alert_on_failure,
                                                    doc_md = """
                                                        Request cartographic data from our database through the API and fill the aggregated scale data
                                                        - Succeed if the cartographic data is fetched and filled in the aggregated scale data
                                                        - Fail if the cartographic data cannot be fetched or filled in the aggregated scale data

                                                        Triggers a callback on failure after 3 retries with a 180 second delay.
                                                          """
                                                    )





save_fetched_cartographic_data = generate_task_python_operator(dag = dag_scale_etl_pipeline,
                                                        task_id = "Save.Fetched.Cartographic.Data",
                                                        python_callable = save_df_to_file,
                                                        op_kwargs = {"task_ids": "Fetch.Cartographic.Data",
                                                                     "savedir": PROCESSING_DATA_DIR,
                                                                     "prefix": "cartographic",
                                                                     "filename": "aggregated_data"
                                                                     },
                                                        retries = 0,
                                                        trigger_rule = "all_success",
                                                        doc_md = """
                                                                Save cartographic aggregated data to a parquet file in the processing dir, ending block 2b tasks
                                                                """
                                                        )





"""
BLOCK 3 - MERGE ALL DATA AND SAVE
"""

load_weather_data = generate_task_python_operator(dag = dag_scale_etl_pipeline,
                                                        task_id = f"Load.Weather.Data",
                                                        python_callable = load_file_as_dataframe,
                                                        op_kwargs = {"path": f"{PROCESSING_DATA_DIR}/weather_aggregated_data.parquet"},
                                                        retries = 3,
                                                        retry_delay = datetime.timedelta(seconds = 10),
                                                        trigger_rule = "all_success",
                                                        on_failure_callback = alert_on_failure,
                                                        doc_md = """
                                                                Load the weather aggregated data parquet file into a DataFrame to continue processing
                                                                    - Succeed if the file is loaded and the DataFrame is not empty
                                                                    - Fail if the file cannot be loaded or the DataFrame is empty
                                                            """
                                                        )



load_cartographic_data = generate_task_python_operator(dag = dag_scale_etl_pipeline,
                                                        task_id = f"Load.Cartographic.Data",
                                                        python_callable = load_file_as_dataframe,
                                                        op_kwargs = {"path": f"{PROCESSING_DATA_DIR}/cartographic_aggregated_data.parquet"},
                                                        retries = 3,
                                                        retry_delay = datetime.timedelta(seconds = 10),
                                                        trigger_rule = "all_success",
                                                        on_failure_callback = alert_on_failure,
                                                        doc_md = """
                                                                Load the cartographic aggregated data parquet file into a DataFrame to continue processing
                                                                    - Succeed if the file is loaded and the DataFrame is not empty
                                                                    - Fail if the file cannot be loaded or the DataFrame is empty
                                                            """
                                                        )



scale_processing_file_loader_block3 = generate_task_python_operator(dag = dag_scale_etl_pipeline,
                                                                    task_id = f"Load.Cleaned.Scale.Data.Block3",
                                                                    python_callable = load_file_as_dataframe,
                                                                    op_kwargs = {"path": f"{PROCESSING_DATA_DIR}/cleaned_scale_data.parquet"},
                                                                    retries = 3,
                                                                    retry_delay = datetime.timedelta(seconds = 10),
                                                                    trigger_rule = "all_success",
                                                                    on_failure_callback = alert_on_failure,
                                                                    doc_md = """
                                                                            Load the cleaned scale data parquet file into a DataFrame to continue processing
                                                                                - Succeed if the file is loaded and the DataFrame is not empty
                                                                                - Fail if the file cannot be loaded or the DataFrame is empty
                                                                        """
                                                                    )


merge_weather_and_cartographic_data = generate_task_python_operator(dag = dag_scale_etl_pipeline,
                                                        task_id = f"Merge.Weather.Cartographic.Data",
                                                        python_callable = join_dataframes,
                                                        op_kwargs = {"task_ids1": "Load.Weather.Data",
                                                                     "task_ids2": "Load.Cartographic.Data",
                                                                     "on_cols": ["lat", "lon"], 
                                                                     "how": "left"},
                                                        retries = 1,
                                                        retry_delay = datetime.timedelta(seconds = 15),
                                                        trigger_rule = "all_success",
                                                        on_failure_callback = alert_on_failure,
                                                        doc_md = """
                                                            Merge weather and cartographic data into a single DataFrame
                                                            """
                                                        )


merge_to_cleaned_data = generate_task_python_operator(dag = dag_scale_etl_pipeline,
                                                        task_id = f"Merged.Data.To.Cleaned.Scale",
                                                        python_callable = join_dataframes,
                                                        op_kwargs = {"task_ids1": "Load.Cleaned.Scale.Data.Block3",
                                                                     "task_ids2": "Merge.Weather.Cartographic.Data",
                                                                     "on_cols": ["date", "lat", "lon"],
                                                                     "how": "left"
                                                                     },
                                                        retries = 1,
                                                        retry_delay = datetime.timedelta(seconds = 15),
                                                        trigger_rule = "all_success",
                                                        on_failure_callback = alert_on_failure,
                                                        doc_md = """
                                                            Merge weather and cartographic data into a single DataFrame
                                                            """
                                                        )



save_final_clean_to_cleaned_directory = generate_task_python_operator(dag = dag_scale_etl_pipeline,
                                                                    task_id = "Save.Final.Cleaned.Data",
                                                                    python_callable = save_df_to_file,
                                                                    op_kwargs = {"task_ids": "Merged.Data.To.Cleaned.Scale",
                                                                                "savedir": CLEANED_DATA_DIR,
                                                                                "prefix": "cleaned",
                                                                                "filename": "data_with_weather_and_cartographic_data"
                                                                                },
                                                                    retries = 0,
                                                                    trigger_rule = "all_success",
                                                                    doc_md = """
                                                                            Save cleaned data with weather and cartographic data to a parquet file in the cleaned data directory
                                                                            """
                                                                    )



clean_processing_directory = generate_task_bash_operator(dag = dag_scale_etl_pipeline,
                                                        task_id = "Clean.Processing.Directory",
                                                        bash_command = f"""
                                                                rm {PROCESSING_DATA_DIR}/*
                                                                """,
                                                        retries = 0,
                                                        trigger_rule = "all_success",
                                                        doc_md = """
                                                                Move raw data files to archives when scale processing is complete
                                                                """
                                                        )



remove_xcom_block_3 = generate_task_python_operator(dag = dag_scale_etl_pipeline,
                                                    task_id = "Remove.Xcom.Block_3",
                                                    python_callable = cleanup_xcom,
                                                    retries = 0,
                                                    trigger_rule = "all_done",
                                                    doc_md = """
                                                        Clean up Xcom data
                                                        """
                                                    )



"""
NEXT DAG TRIGERRER
"""
next_dag_triggerer = generate_task_trigger_dag_operator(dag = dag_scale_etl_pipeline,
                                                        task_id = "Trigger.Next.DAG",
                                                        trigger_dag_id = "segmented_etl_pipeline",
                                                        retries = 0,
                                                        trigger_rule = "all_success",
                                                        on_success_callback = None,
                                                        on_failure_callback = None,
                                                        doc_md = """
                                                            Trigger the next DAG in the pipeline
                                                            """)
"""
DEPENDENCIES
"""
# BLOCK 1 Dependencies
raw_file_sensor >> raw_file_loader >> scale_data_cleaner >> save_cleaned_scale_data
save_cleaned_scale_data >> remove_xcom_block_1
save_cleaned_scale_data >> move_raw_files_to_archives
# BLOCK 2 Dependencies
save_cleaned_scale_data >> scale_processing_file_loader_block2 >> generate_aggregated_scale_data
save_fetched_weather_data >> remove_xcom_block_2
save_fetched_cartographic_data >> remove_xcom_block_2
# BLOCK 2a Dependencies
generate_aggregated_scale_data >> prepare_data_to_request_weather_data >> fetch_and_fill_weather_data >> save_fetched_weather_data
# BLOCK 2b Dependencies
generate_aggregated_scale_data >> prepare_aggregated_cartographic_data >> request_cartographic_data >> save_fetched_cartographic_data
# BLOCK 3 Dependencies
save_fetched_weather_data >> load_weather_data >> merge_weather_and_cartographic_data
save_fetched_cartographic_data >> load_cartographic_data >> merge_weather_and_cartographic_data
merge_weather_and_cartographic_data >> merge_to_cleaned_data
remove_xcom_block_2 >> scale_processing_file_loader_block3 >> merge_to_cleaned_data
merge_to_cleaned_data >> save_final_clean_to_cleaned_directory
save_final_clean_to_cleaned_directory >> clean_processing_directory
save_final_clean_to_cleaned_directory >> remove_xcom_block_3
# NEXT DAG TRIGGERER
remove_xcom_block_3 >> next_dag_triggerer
clean_processing_directory >> next_dag_triggerer