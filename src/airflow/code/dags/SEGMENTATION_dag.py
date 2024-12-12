#airflow/code/dags/SEGMENTATION_dag.py

"""
SEGMENTATION DAG - Execute ETL pipeline to process cleaned data to segmented data used for deep analysis and machine learning

Steps:
1. Load cleaned data file
2. Apply segmentation (piecewise linear regression)
3. Save all segmentation models and segmented data to final table
4. Trigger the next DAG in the pipeline
"""

# LIB
from airflow import DAG
from airflow.utils.dates import days_ago

import datetime


from utils.callbacks import alert_on_failure
from utils.config import CLEANED_DATA_DIR
from utils.config import SEGMENTATION_MIN_MONTH, SEGMENTATION_MAX_MONTH, SEGMENTATION_MODEL_DIR
from utils.operators import generate_task_python_operator, generate_task_trigger_dag_operator, generate_task_bash_operator

# Generic functions
from utils.generic_functions import load_file_as_dataframe, save_df_to_file, cleanup_xcom
# Segmentation functions
from utils.segmentation_functions import df_segmentation_operation



"""
DAG Declaration
"""
dag_segmented_etl_pipeline = DAG(
    dag_id = "segmented_etl_pipeline",
    description = "Execute ETL pipeline to process cleaned data to segmented data used for deep analysis and machine learning",
    tags = ["ETL", "data"],
    catchup = False,
    schedule_interval =  None,
    start_date = days_ago(1),
    doc_md = """
        SEGMENTATION DAG - Execute ETL pipeline to process cleaned data to segmented data used for deep analysis and machine learning

        Steps:
        1. Load cleaned data file
        2. Apply segmentation (piecewise linear regression)
        3. Save all segmentation models and segmented data to final table
        4. Trigger the next DAG in the pipeline
    """
)



"""
TASKS
"""


"""
BLOCK 1 - LOAD CLEANED DATA | APPLY SEGMENTATION | AGGREGATE WEATHER INDICATORS | JOIN CARTOGRAPHIC DATA | SAVE SEGMENTED DATA
"""
cleaned_scale_data_loader = generate_task_python_operator(dag = dag_segmented_etl_pipeline,
                                                        task_id = f"Load.Cleaned.Data",
                                                        python_callable = load_file_as_dataframe,
                                                        op_kwargs = {"path": f"{CLEANED_DATA_DIR}/cleaned_data_with_weather_and_cartographic_data.parquet"},
                                                        retries = 3,
                                                        retry_delay = datetime.timedelta(seconds = 10),
                                                        trigger_rule = "all_success",
                                                        on_failure_callback = alert_on_failure,
                                                        doc_md = """
                                                            Load cleaned data from a file
                                                            """
                                                        )



apply_segmentation_on_data = generate_task_python_operator(dag = dag_segmented_etl_pipeline,
                                                        task_id = f"Apply.Segmentation",
                                                        python_callable = df_segmentation_operation,
                                                        op_kwargs = {"task_ids": "Load.Cleaned.Data",
                                                                     "segmentation_min_month": SEGMENTATION_MIN_MONTH,
                                                                     "segmentation_max_month": SEGMENTATION_MAX_MONTH,
                                                                     "model_savedir": SEGMENTATION_MODEL_DIR,
                                                                     },
                                                        retries = 0,
                                                        trigger_rule = "all_success",
                                                        on_failure_callback = alert_on_failure,
                                                        doc_md = """
                                                            Apply segmentation on the loaded data and return segmented data
                                                            """
                                                        )


save_segmented_model = generate_task_bash_operator(dag = dag_segmented_etl_pipeline,
                                        task_id = "Save.Segmentation.Model",
                                        bash_command = "echo 'Mock Task'",
                                        retries = 0,
                                        on_success_callback = None,
                                        on_failure_callback = None,
                                        doc_md = """
                                            Save the segmentation model for each scale to a file
                                            """)


save_segmented_data = generate_task_python_operator(dag = dag_segmented_etl_pipeline,
                                                    task_id = "Save.Segmented.Data",
                                                    python_callable = save_df_to_file,
                                                    op_kwargs = {"task_ids": "Apply.Segmentation",
                                                                "savedir": CLEANED_DATA_DIR,
                                                                "prefix": "segmented",
                                                                "filename": "data"
                                                                },
                                                    retries = 0,
                                                    trigger_rule = "all_success",
                                                    doc_md = """
                                                        Save the segmented data to a file for further analysis
                                                            """
                                                    )


remove_xcom = generate_task_python_operator(dag = dag_segmented_etl_pipeline,
                                            task_id = "Remove.Xcom.",
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
next_dag_triggerer = generate_task_trigger_dag_operator(dag = dag_segmented_etl_pipeline,
                                                        task_id = "next_dag_triggerer",
                                                        trigger_dag_id = "ml_pipeline",
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
cleaned_scale_data_loader >> apply_segmentation_on_data 

apply_segmentation_on_data >> save_segmented_data
apply_segmentation_on_data >> save_segmented_model
save_segmented_data >> remove_xcom
save_segmented_model >> remove_xcom
remove_xcom >> next_dag_triggerer

