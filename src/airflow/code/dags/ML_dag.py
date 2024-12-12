#airflow/code/dags/SEGMENTATION_dag.py

"""
MACHINE LEARNING DAG - Execute ML pipeline to process segmented data and train a model

Steps:
1. Load segmented data
2. preprocessdataing
3.
4.
5.
"""

# LIB
from airflow import DAG
from airflow.utils.dates import days_ago

import datetime


from utils.callbacks import alert_on_failure
from utils.config import CLEANED_DATA_DIR, MLFLOW_TRACKING_URI
from utils.config import DF_FILLNA_DEFAULT_VALUE, TARGET_COMLUMN, COLUMNS_TO_ENCODE, OTHER_COL_TO_DROP, ML_MODEL_CHOICE, MODEL_TEST_PARAMS
from utils.operators import generate_task_python_operator



# Generic functions
from utils.generic_functions import load_file_as_dataframe, fillna_dataframe, cleanup_xcom
# ML functions
from utils.ml_functions import get_features_target, split_data, encode_categorical_features, scale_features, create_model, train_model, get_model_scores, run_mlflow_experiment, tag_best_model


"""
DAG Declaration
"""
dag_ml_pipeline = DAG(
    dag_id = "ml_pipeline",
    description = "Execute ML pipeline to process segmented data and train a model",
    tags = ["Machine Learning"],
    catchup = False,
    schedule_interval =  None,
    start_date = days_ago(1),
    doc_md = """
        MACHINE LEARNING DAG - Execute ML pipeline to process segmented data and train a model

        Steps:
        1. Load segmented data from a file
        2. Preprocess data (fillna, split, encode, scale)
        3. Train Grid models
        4. Get model scores
        5. Run MLFlow experiment
    """
)



"""
TASKS
"""

"""
BLOCK 1 - LOAD DATA
"""
segmented_scale_data_loader = generate_task_python_operator(dag = dag_ml_pipeline,
                                                        task_id = f"Load.Segmented.Data",
                                                        python_callable = load_file_as_dataframe,
                                                        op_kwargs = {"path": f"{CLEANED_DATA_DIR}/segmented_data.parquet"},
                                                        retries = 3,
                                                        retry_delay = datetime.timedelta(seconds = 10),
                                                        trigger_rule = "all_success",
                                                        on_failure_callback = alert_on_failure,
                                                        doc_md = """
                                                            Load segmented data from a file
                                                            """
                                                        )


"""
BLOCK 2 - DATA PREPROCESSING
"""
preprocessing_data_fillna = generate_task_python_operator(dag = dag_ml_pipeline,
                                                          task_id = f"Preprocessing.Fillna",
                                                          python_callable = fillna_dataframe,
                                                          op_kwargs = {"task_ids": "Load.Segmented.Data",
                                                                       "default_value": DF_FILLNA_DEFAULT_VALUE
                                                                       },
                                                          retries = 0,
                                                          trigger_rule = "all_success",
                                                          on_failure_callback = alert_on_failure,
                                                            doc_md = """
                                                            Fill NA values in the data with a default value
                                                            """
                                                            )


features_target = generate_task_python_operator(dag = dag_ml_pipeline,
                                                task_id = f"Get.Features.Target",
                                                python_callable = get_features_target,
                                                op_kwargs = {"task_ids": "Preprocessing.Fillna",
                                                                "target_column": TARGET_COMLUMN,
                                                                "other_col_to_drop": OTHER_COL_TO_DROP},
                                                retries = 0,
                                                trigger_rule = "all_success",
                                                on_failure_callback = alert_on_failure,
                                                doc_md = """
                                                Drop unnecessary columns and get features and target
                                                """
                                                    )


splitted_data = generate_task_python_operator(dag = dag_ml_pipeline,
                                            task_id = f"Split.Data",
                                            python_callable = split_data,
                                            op_kwargs = {"task_ids": "Get.Features.Target",
                                                         "train_size": 0.8,
                                                         "test_size": 0.2,
                                                         "shuffle": False,
                                                         "random_state": 42
                                                        },
                                            retries = 0,
                                            trigger_rule = "all_success",
                                            on_failure_callback = alert_on_failure,
                                            doc_md = """
                                            Split data into train and test sets
                                            """
                                            )



data_encoder = generate_task_python_operator(dag = dag_ml_pipeline,
                                            task_id = f"Encode.Categorical.Features",
                                            python_callable = encode_categorical_features,
                                            op_kwargs = {"task_ids": "Split.Data",
                                                         "columns_to_encode": COLUMNS_TO_ENCODE},
                                            retries = 0,
                                            trigger_rule = "all_success",
                                            on_failure_callback = alert_on_failure,
                                            doc_md = """
                                            Encode categorical features based on a predefined list
                                            """
                                            )


data_scaler = generate_task_python_operator(dag = dag_ml_pipeline,
                                            task_id = f"Scale.Features",
                                            python_callable = scale_features,
                                            op_kwargs = {"task_ids": "Encode.Categorical.Features"},
                                            retries = 0,
                                            trigger_rule = "all_success",
                                            on_failure_callback = alert_on_failure,
                                            doc_md = """
                                            Scale features using StandardScaler
                                            """
                                            )



"""
BLOCK 3 - MACHINE LEARNING
"""
model_declarators = []
for defined_model, model_test_param in zip(ML_MODEL_CHOICE, MODEL_TEST_PARAMS):

    create_model_object = generate_task_python_operator(dag = dag_ml_pipeline,
                                                        task_id = f"Create.{defined_model}.Model",
                                                        python_callable = create_model,
                                                        op_kwargs = {"model_choice": defined_model,
                                                                     "cv": 2,
                                                                     "param_grid": model_test_param},
                                                        retries = 0,
                                                        trigger_rule = "all_success",
                                                        doc_md = """
                                                            Create a model object for each model in the model choice variable
                                                            """
                                                        )

    model_declarators.append(create_model_object)




model_trainers = []
for defined_model in ML_MODEL_CHOICE:

    fit_grid_model = generate_task_python_operator(dag = dag_ml_pipeline,
                                                    task_id = f"Fit.Grid.{defined_model}.Model",
                                                    python_callable = train_model,
                                                    op_kwargs = {"task_ids_model": f"Create.{defined_model}.Model",
                                                                 "task_ids_data": "Scale.Features"},
                                                    retries = 0,
                                                    trigger_rule = "all_success",
                                                    doc_md = """
                                                    Fit the chosen model
                                                        """
                                                    )

    model_trainers.append(fit_grid_model)






model_metrics = []
for defined_model in ML_MODEL_CHOICE:

    model_scores = generate_task_python_operator(dag = dag_ml_pipeline,
                                                task_id = f"Get.Scores.{defined_model}.Model",
                                                python_callable = get_model_scores,
                                                op_kwargs = {"task_ids_fitted_model": f"Fit.Grid.{defined_model}.Model",
                                                                "task_ids_data": "Scale.Features"},
                                                retries = 0,
                                                trigger_rule = "all_success",
                                                doc_md = """
                                                Get model metrics
                                                    """
                                                )

    model_metrics.append(model_scores)




"""
BLOCK 4 - MLFLOW
"""
model_runs = []
for defined_model in ML_MODEL_CHOICE:


    mlflow_runs = generate_task_python_operator(dag = dag_ml_pipeline,
                                                task_id = f"MLFlow.Run.{defined_model}.Model",
                                                python_callable = run_mlflow_experiment,
                                                op_kwargs = {
                                                    "task_ids_data": "Scale.Features",
                                                    "task_ids_fitted_model": f"Fit.Grid.{defined_model}.Model",
                                                    "task_ids_scores": f"Get.Scores.{defined_model}.Model",
                                                    "experiment_name": f"experiment_{defined_model}",
                                                    "model_name": defined_model,
                                                    "training_tag": "partial"},
                                                retries = 0,
                                                trigger_rule = "all_success",
                                                doc_md = """
                                                Run MLFlow experiment
                                                    """
                                                )

    model_runs.append(mlflow_runs)



mlflow_best_model = generate_task_python_operator(dag = dag_ml_pipeline,
                                                task_id = f"MLFlow.Tag.Best.Model",
                                                python_callable = tag_best_model,
                                                op_kwargs = {},
                                                retries = 0,
                                                trigger_rule = "all_success",
                                                doc_md = """
                                                Tag the best model in MLFlow
                                                    """
                                                )




"""
CLEANUP XCOM
"""

remove_xcom = generate_task_python_operator(dag = dag_ml_pipeline,
                                            task_id = "Remove.Xcom",
                                            python_callable = cleanup_xcom,
                                            retries = 0,
                                            trigger_rule = "all_done",
                                            doc_md = """
                                                Clean up Xcom data
                                                """
                                            )




"""
DEPENDENCIES
"""
# BLOCK 2
segmented_scale_data_loader >> preprocessing_data_fillna >> features_target >> splitted_data >> data_encoder >> data_scaler

# BLOCK 2
for model_declarator, model_trainer, model_metric, model_run in zip(model_declarators, model_trainers, model_metrics, model_runs):
    data_scaler >> model_declarator >> model_trainer >> model_metric >> model_run

for model_run in model_runs:
    model_run >> remove_xcom >> mlflow_best_model