import os
import pickle
from dataclasses import dataclass
from typing import List

import numpy as np
import pandas as pd
from prefect import flow, task
from scipy.sparse import csr_matrix
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


@dataclass
class Config:
    TRAIN_DATA = "../data/yellow_tripdata_2021-01.parquet"
    TEST_DATA = "../data/yellow_tripdata_2021-02.parquet"
    INFERENCE_DATA = "../data/yellow_tripdata_2021-03.parquet"
    LOCAL_STORAGE = './results'
    CATEGORICAL_VARS = ['PULocationID', 'DOLocationID', 'passenger_count']


@task(name='load_data', tags=['preprocessing'], retries=2, retry_delay_seconds=60)
def load_data(path: str) -> pd.DataFrame:
    return pd.read_parquet(path)


@task(name='compute_duration', tags=['preprocessing'])
def compute_target(
        df: pd.DataFrame,
        pickup_column: str = "tpep_pickup_datetime",
        dropoff_column: str = "tpep_dropoff_datetime"
) -> pd.DataFrame:
    """
    Compute the trip duration in minutes based
    on pickup and dropoff time
    """
    df["duration"] = df[dropoff_column] - df[pickup_column]
    df["duration"] = df["duration"].dt.total_seconds() / 60
    return df


@task(name='filter_outliers', tags=['preprocessing'])
def filter_outliers(
        df: pd.DataFrame,
        min_duration: int = 1,
        max_duration: int = 60
) -> pd.DataFrame:
    """
    Remove rows corresponding to negative/zero
    and too high target' values from the dataset
    """
    return df[df['duration'].between(min_duration, max_duration)]


@task(name='encode_cat_cols', tags=['preprocessing'])
def encode_categorical_cols(
        df: pd.DataFrame,
        categorical_cols: List[str] = None
) -> pd.DataFrame:
    """
    Takes a Pandas dataframe and a list of categorical
    column names, and returns dataframe with
    the specified columns converted to categorical data type
    """
    if categorical_cols is None:
        categorical_cols = Config.CATEGORICAL_VARS
    df[categorical_cols] = df[categorical_cols].fillna(-1).astype('int')
    df[categorical_cols] = df[categorical_cols].astype('str')
    return df


@task(name='extract_x_y', tags=['preprocessing'])
def extract_x_y(
        df: pd.DataFrame,
        categorical_cols: List[str] = None,
        dv: DictVectorizer = None,
        with_target: bool = True
) -> dict:
    """
    Turns lists of mappings (dicts of feature names to feature values)
    into sparse matrices for use with scikit-learn estimators
    using Dictvectorizer object.
    :return The sparce matrix, the target' values if needed and the
    dictvectorizer object.
    """
    if categorical_cols is None:
        categorical_cols = Config.CATEGORICAL_VARS
    dicts = df[categorical_cols].to_dict(orient='records')

    y = None
    if with_target:
        if dv is None:
            dv = DictVectorizer()
            dv.fit(dicts)
        y = df["duration"].values

    x = dv.transform(dicts)
    return {'x': x, 'y': y, 'dv': dv}


@flow(name="Data processing", retries=1, retry_delay_seconds=30)
def process_data(path: str,  dv=None, with_target: bool = True) -> dict:
    """
    Load data from a parquet file
    Compute target(duration column) and apply threshold filters (optional)
    Turn features to sparce matrix
    :return The sparce matrix, the target' values and the
    dictvectorizer object if needed.
    """
    df = load_data(path)
    if with_target:
        df1 = compute_target(df)
        df2 = filter_outliers(df1)
        df3 = encode_categorical_cols(df2)
        return extract_x_y(df3, dv=dv)
    else:
        df1 = encode_categorical_cols(df)
        return extract_x_y(df1, dv=dv, with_target=with_target)
    

@task(name="Train model", tags=['Model'])
def train_model(
        x_train: csr_matrix,
        y_train: np.ndarray
) -> LinearRegression:
    """Train and return a linear regression model"""
    lr = LinearRegression()
    lr.fit(x_train, y_train)
    return lr


@task(name="Make prediction", tags=["Model"])
def predict_duration(
        input_data: csr_matrix,
        model: LinearRegression
) -> np.ndarray:
    """
    Use trained linear regression model
    to predict target from input data
    :return array of predictions
    """
    return model.predict(input_data)


@task(name="Evaluation", tags=["Model"])
def evaluate_model(
        y_true: np.ndarray,
        y_pred: np.ndarray
) -> float:
    """Calculate mean squared error for two arrays"""
    return mean_squared_error(y_true, y_pred, squared=False)


@task(name="Load", tags=['Serialize'])
def load_pickle(path: str):
    with open(path, 'rb') as f:
        loaded_obj = pickle.load(f)
    return loaded_obj


@task(name="Save", tags=['Serialize'])
def save_pickle(path: str, obj: dict):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)

        
@flow(name="Model initialisation")
def train_and_predict(
        x_train,
        y_train,
        x_test,
        y_test
) -> dict:
    """Train model, predict values and calculate error"""
    model = train_model(x_train, y_train)
    prediction = predict_duration(x_test, model)
    mse = evaluate_model(y_test, prediction)
    return {'model': model, 'mse': mse}


@flow(name="Example Machine learning workflow", retries=1, retry_delay_seconds=30)
def complete_ml(
        train_path: str,
        test_path: str,
        save_model: bool = True,
        save_dv: bool = True,
        local_storage: str = Config.LOCAL_STORAGE
) -> None:
    """
    Load data and prepare sparse matrix (using dictvectorizer) for model training
    Train model, make predictions and calculate error
    Save model and dictvectorizer to a folder in pickle format
    :return none
    """
    if not os.path.exists(local_storage):
        os.makedirs(local_storage)

    train_data = process_data(train_path)
    test_data = process_data(test_path, dv=train_data["dv"])
    model_obj = train_and_predict(train_data["x"], train_data["y"], test_data['x'], test_data['y'])
    if save_model:
        save_pickle(f"{local_storage}/model.pickle", model_obj)
    if save_dv:
        save_pickle(f"{local_storage}/dv.pickle", train_data["dv"])


@flow(name="Batch inference", retries=1, retry_delay_seconds=30)
def batch_inference(input_path, dv=None, model=None, local_storage=Config.LOCAL_STORAGE):
    """
    Load model and dictvectorizer from folder
    Transforms input data with dictvectorizer
    Predict values using loaded model
    :return array of predictions
    """
    if not dv:
        dv = load_pickle(f"{local_storage}/dv.pickle")
    data = process_data(input_path, dv, with_target=False)
    if not model:
        model = load_pickle(f"{local_storage}/model.pickle")["model"]
    return predict_duration(data["x"], model)
