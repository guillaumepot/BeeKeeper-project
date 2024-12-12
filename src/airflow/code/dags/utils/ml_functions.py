#airflow/code/dags/ml_functions.py



# LIB
import datetime
import os
import pandas as pd
import pickle


# Data preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Models
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV


# Metrics
from sklearn.metrics import mean_squared_error as MSE
from sklearn.metrics import mean_absolute_error as MAE

# Mlfow
from mlflow import MlflowClient
import mlflow


from utils.config import MLFLOW_TRACKING_URI



"""
MACHINE LEARNING FUNCTIONS
"""


# DATA PREPROCESSING FUNCTIONS
def get_features_target(**kwargs) -> tuple:
    """
    Extracts features and target from a DataFrame passed via Airflow's XCom.
    Args:
        **kwargs: Arbitrary keyword arguments.
            - task_instance: The Airflow task instance used to pull XCom data.
            - task_ids: The task ID from which to pull the DataFrame.
            - target_column: The name of the column to be used as the target.
            - other_col_to_drop: A list of columns to be dropped from the DataFrame.
    Returns:
        tuple: A tuple containing:
            - features (pd.DataFrame): The DataFrame with the specified columns dropped.
            - target (list): The target column converted to a list.
    """

    task_instance = kwargs.get('task_instance')
    df = task_instance.xcom_pull(task_ids = kwargs["task_ids"])

    target = df[kwargs["target_column"]]
    cols_to_drop = [col for col in kwargs["other_col_to_drop"] if col in df.columns]
    features = df.drop(cols_to_drop, axis = 1)


    return (features, target.to_list())



def split_data(**kwargs) -> tuple:
    """
    Splits the dataset into training and testing sets.

    This function retrieves the features and target data from an Airflow task instance
    using XCom, and then splits the data into training and testing sets using 
    scikit-learn's train_test_split function.

    Args:
        **kwargs: Arbitrary keyword arguments.
            - task_instance: The Airflow task instance from which to pull data.
            - task_ids: The task ID from which to pull the XCom data.
            - test_size: The proportion of the dataset to include in the test split.
            - shuffle: Whether or not to shuffle the data before splitting.
            - random_state: Controls the shuffling applied to the data before the split.

    Returns:
        tuple: A tuple containing the training and testing data:
            - X_train: Training features.
            - X_test: Testing features.
            - y_train: Training target values as a list.
            - y_test: Testing target values as a list.
    """
    task_instance = kwargs.get('task_instance')
    features_target_tuple = task_instance.xcom_pull(task_ids = kwargs["task_ids"])

    features = features_target_tuple[0]
    target = pd.Series(features_target_tuple[1])

    X_train, X_test, y_train, y_test = train_test_split(features, target,
                                                        test_size = kwargs["test_size"],
                                                        shuffle = kwargs["shuffle"],
                                                        random_state = kwargs["random_state"])



    return (X_train, X_test, y_train.to_list(), y_test.to_list())




def encode_categorical_features(**kwargs) -> tuple:
    """
    Encodes categorical features in training and testing datasets using LabelEncoder.

    Args:
        **kwargs: Arbitrary keyword arguments. Expected keys are:
            - task_instance: The task instance from which to pull data using XCom.
            - task_ids: The task IDs to pull data from.
            - columns_to_encode: List of column names to encode.

    Returns:
        tuple: A tuple containing:
            - X_train_encoded (pd.DataFrame): The encoded training dataset.
            - X_test_encoded (pd.DataFrame): The encoded testing dataset.
            - y_train (list): The training labels as a list.
            - y_test (list): The testing labels as a list.
            - encoder (LabelEncoder): The fitted LabelEncoder instance.
    """

    task_instance = kwargs.get('task_instance')
    splitted_data = task_instance.xcom_pull(task_ids = kwargs["task_ids"])


    X_train_encoded = splitted_data[0]
    X_test_encoded = splitted_data[1]
    y_train = pd.Series(splitted_data[2])
    y_test = pd.Series(splitted_data[3])


    encoder = LabelEncoder()
    X_train_encoded[kwargs["columns_to_encode"]] = encoder.fit_transform(X_train_encoded[kwargs["columns_to_encode"]])
    X_test_encoded[kwargs["columns_to_encode"]] = encoder.transform(X_test_encoded[kwargs["columns_to_encode"]])

    return (X_train_encoded, X_test_encoded, y_train.to_list(), y_test.to_list(), encoder)



def scale_features(**kwargs) -> tuple:
    """
    Scales the features of the training and test datasets using StandardScaler.

    Args:
        **kwargs: Arbitrary keyword arguments. Expected keys are:
            - task_instance: The task instance from which to pull XCom data.
            - task_ids: The task IDs to pull the XCom data from.

    Returns:
        tuple: A tuple containing:
            - X_train_encoded_scaled (ndarray): Scaled training features.
            - X_test_encoded_scaled (ndarray): Scaled test features.
            - y_train (list): Training labels.
            - y_test (list): Test labels.
            - encoder: The encoder used for encoding the features.
            - scaler: The StandardScaler instance used for scaling the features.
    """
    task_instance = kwargs.get('task_instance')
    encoded_data = task_instance.xcom_pull(task_ids = kwargs["task_ids"])

    X_train_encoded = encoded_data[0]
    X_test_encoded = encoded_data[1]
    y_train = pd.Series(encoded_data[2])
    y_test = pd.Series(encoded_data[3])
    encoder = encoded_data[4]


    scaler = StandardScaler()
    X_train_encoded_scaled = scaler.fit_transform(X_train_encoded)
    X_test_encoded_scaled = scaler.transform(X_test_encoded)


    return (X_train_encoded_scaled, X_test_encoded_scaled, y_train.to_list(), y_test.to_list(), encoder, scaler)





# MODEL DEFINITION FUNCTIONS
def create_model(**kwargs):
    """
    Create a machine learning model based on the specified model choice and parameters.

    Parameters:
    kwargs (dict): A dictionary of keyword arguments containing:
        - model_choice (str): The choice of model to create. Options are "RandomForestRegressor", "LinearRegression", or "SVR".
        - param_grid (dict): The parameter grid to use for GridSearchCV.
        - cv (int): The number of cross-validation folds to use in GridSearchCV.

    Returns:
    GridSearchCV: A GridSearchCV object with the specified model and parameters.
    """
    if kwargs["model_choice"] == "RandomForestRegressor":
        model = RandomForestRegressor()
    elif kwargs["model_choice"] == "LinearRegression":
        model = LinearRegression()
    elif kwargs["model_choice"] == "SVR":
        model = SVR()


    model_grid = GridSearchCV(model, kwargs["param_grid"], cv = kwargs["cv"], n_jobs = -1)


    return model_grid




def choose_best_model(**kwargs):
    """
    Chooses the best model by fitting a grid search model on the training data.

    Args:
        **kwargs: Arbitrary keyword arguments. Expected keys are:
            - task_instance: The Airflow task instance.
            - task_ids_model: The task ID from which to pull the grid search model.
            - task_ids_data: The task ID from which to pull the training data.

    Returns:
        The fitted grid search model.
    """
    task_instance = kwargs.get('task_instance')
    grid_model = task_instance.xcom_pull(task_ids = kwargs["task_ids_model"])
    X_train_encoded_scaled = task_instance.xcom_pull(task_ids = kwargs["task_ids_data"])[0]
    y_train = pd.Series(task_instance.xcom_pull(task_ids = kwargs["task_ids_data"])[2])

    grid_model.fit(X_train_encoded_scaled, y_train)

    return grid_model




# TRAINING FUNCTIONS
def train_model(**kwargs):
    """
    Trains a machine learning model using the provided training data and model.

    Args:
        **kwargs: Arbitrary keyword arguments. Expected keys are:
            - task_instance: The task instance object from which to pull XCom data.
            - task_ids_model: The task ID from which to pull the model.
            - task_ids_data: The task ID from which to pull the training data.

    Returns:
        The trained machine learning model.
    """
    task_instance = kwargs.get('task_instance')
    grid_model = task_instance.xcom_pull(task_ids = kwargs["task_ids_model"])
    X_train_encoded = task_instance.xcom_pull(task_ids = kwargs["task_ids_data"])[0]
    y_train = pd.Series(task_instance.xcom_pull(task_ids = kwargs["task_ids_data"])[2])


    grid_model.fit(X_train_encoded, y_train)

    return grid_model



# MODEL EVALUATION
def get_model_scores(**kwargs) -> tuple:
    """
    Retrieve model scores and parameters from an Airflow task instance.

    This function pulls the fitted model and test data from XCom, makes predictions,
    and calculates various performance metrics.

    Args:
        **kwargs: Arbitrary keyword arguments. Expected keys are:
            - task_instance: The Airflow task instance.
            - task_ids_fitted_model: The task ID for the fitted model.
            - task_ids_data: The task ID for the test data.

    Returns:
        tuple: A tuple containing the following elements:
            - fitted_model_best_params (dict): The best parameters of the fitted model.
            - fitted_model_best_score (float): The best score of the fitted model.
            - fitted_model_mae (float): The Mean Absolute Error (MAE) of the model predictions.
            - fitted_model_mse (float): The Mean Squared Error (MSE) of the model predictions.
    """
    task_instance = kwargs.get('task_instance')
    fitted_model = task_instance.xcom_pull(task_ids = kwargs["task_ids_fitted_model"])
    X_test_encoded_scaled = task_instance.xcom_pull(task_ids = kwargs["task_ids_data"])[1]
    y_test = pd.Series(task_instance.xcom_pull(task_ids = kwargs["task_ids_data"])[3])

    y_pred = fitted_model.predict(X_test_encoded_scaled)


    fitted_model_best_params = fitted_model.best_params_
    fitted_model_best_score = fitted_model.best_score_
    fitted_model_mae = MAE(y_test, y_pred)
    fitted_model_mse = MSE(y_test, y_pred)

    return (fitted_model_best_params, fitted_model_best_score, fitted_model_mae, fitted_model_mse)





# MLFLOW FUNCTIONS
def run_mlflow_experiment(**kwargs) -> None:
    """
    Runs an MLflow experiment by logging model parameters, metrics, and artifacts.
    Parameters:
    -----------
    **kwargs : dict
        A dictionary of keyword arguments containing the following keys:
        - experiment_name (str): The name of the MLflow experiment.
        - task_instance (TaskInstance): The Airflow task instance.
        - task_ids_fitted_model (str): The task ID for retrieving the fitted model.
        - task_ids_scores (str): The task ID for retrieving the model scores.
        - task_ids_data (str): The task ID for retrieving the training and testing data.
        - model_name (str): The name to register the model under in MLflow.
        - training_tag (str): A tag to associate with the MLflow run.
    Returns:
    --------
    None
    """
    # MLFLOW configuration
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(kwargs["experiment_name"])

    date = datetime.datetime.now().strftime("%Y%m%d")
    run_name = f"{kwargs["experiment_name"]}_{date}"

    artifact_path = f"artifacts_{run_name}"

   
    # Retreive objects
    task_instance = kwargs.get('task_instance')
    fitted_model = task_instance.xcom_pull(task_ids = kwargs["task_ids_fitted_model"])

    fitted_model_best_params = task_instance.xcom_pull(task_ids = kwargs["task_ids_scores"])[0]
    fitted_model_best_score = task_instance.xcom_pull(task_ids = kwargs["task_ids_scores"])[1]
    fitted_model_mae = task_instance.xcom_pull(task_ids = kwargs["task_ids_scores"])[2]
    fitted_model_mse = task_instance.xcom_pull(task_ids = kwargs["task_ids_scores"])[3]

    X_train_encoded = task_instance.xcom_pull(task_ids = kwargs["task_ids_data"])[0]
    X_test_encoded_scaled = task_instance.xcom_pull(task_ids = kwargs["task_ids_data"])[1]
    y_train = pd.Series(task_instance.xcom_pull(task_ids = kwargs["task_ids_data"])[2])
    y_test = pd.Series(task_instance.xcom_pull(task_ids = kwargs["task_ids_data"])[3])
    encoder = task_instance.xcom_pull(task_ids = kwargs["task_ids_data"])[4]
    scaler = task_instance.xcom_pull(task_ids = kwargs["task_ids_data"])[5]


    if not os.path.exists(f"{MLFLOW_TRACKING_URI}/sklearn_objects_{run_name}"):
        os.makedirs(f"{MLFLOW_TRACKING_URI}/sklearn_objects_{run_name}")
    object_path = f"{MLFLOW_TRACKING_URI}/sklearn_objects_{run_name}"
    encoder_path = f"{object_path}/encoder.pkl"
    scaler_path = f"{object_path}/scaler.pkl"

    client = MlflowClient()



    pickle.dump(encoder, open(encoder_path, "wb"))
    pickle.dump(scaler, open(scaler_path, "wb"))


    # Convert numpy arrays to pandas DataFrames or Series
    X_train_encoded = pd.DataFrame(task_instance.xcom_pull(task_ids=kwargs["task_ids_data"])[0])
    X_test_encoded_scaled = pd.DataFrame(task_instance.xcom_pull(task_ids=kwargs["task_ids_data"])[1])
    y_train = pd.Series(task_instance.xcom_pull(task_ids=kwargs["task_ids_data"])[2])
    y_test = pd.Series(task_instance.xcom_pull(task_ids=kwargs["task_ids_data"])[3])


    # Save data to files
    X_train_encoded_path = f"{object_path}/X_train_encoded.pkl"
    X_test_encoded_scaled_path = f"{object_path}/X_test_encoded_scaled.pkl"
    y_train_path = f"{object_path}/y_train.pkl"
    y_test_path = f"{object_path}/y_test.pkl"

    X_train_encoded.to_pickle(X_train_encoded_path)
    X_test_encoded_scaled.to_pickle(X_test_encoded_scaled_path)
    y_train.to_pickle(y_train_path)
    y_test.to_pickle(y_test_path)



    # Store information in Mlflow Data
    with mlflow.start_run(run_name = run_name) as run:

        # Save the encoder and the scaler
        mlflow.log_artifact(encoder_path, artifact_path)
        mlflow.log_artifact(scaler_path, artifact_path)

        # Save the data
        mlflow.log_artifact(X_train_encoded_path, artifact_path)
        mlflow.log_artifact(X_test_encoded_scaled_path, artifact_path)
        mlflow.log_artifact(y_train_path, artifact_path)
        mlflow.log_artifact(y_test_path, artifact_path)



        # Model Data
        mlflow.sklearn.log_model(sk_model = fitted_model,
                                input_example = X_train_encoded,
                                artifact_path = artifact_path,
                                registered_model_name = kwargs["model_name"])
        

        for param_name, param_value in fitted_model_best_params.items():
            mlflow.log_param(param_name, param_value)

        mlflow.log_metric("R²", fitted_model_best_score)
        mlflow.log_metric("MAE", fitted_model_mae)
        mlflow.log_metric("MSE", fitted_model_mse)

        # Tag the run
        client.set_tag(run.info.run_id, "training", kwargs["training_tag"])



def tag_best_model(**kwargs) -> None:
    """
    Tags the best model among all registered models in MLflow.
    This function performs the following steps:
    1. Retrieves all registered models from MLflow.
    2. Sets the "best_model" tag to "False" for all models.
    3. Identifies the model with the highest score.
    4. Sets the "best_model" tag to "True" for the model with the highest score.
    Args:
        **kwargs: Arbitrary keyword arguments.
    """
    client = MlflowClient()
    
    # Get all registered models
    registered_models = client.search_registered_models()

    best_model = None
    best_score = float('-inf')

    # Set all tags "best_model" to False
    for model in registered_models:
        client.set_tag(
                        name = model.name,
                        version = model.latest_versions[0].version,
                        key = "best_model",
                        value = "False"
                        )

    # Get the best model and tag it "True"
    for model in registered_models:
        model_name = model.name
        model_version = model.latest_versions[0].version
        model_uri = model.latest_versions[0].source
        model_score = model.latest_versions[0].run_id

        if model_score > best_score:
            best_model = model_name
            best_score = model_score

    if best_model:
        client.set_tag(
                        name = best_model.name,
                        version = best_model.version,
                        key = "best_model",
                        value = "True"
                        )