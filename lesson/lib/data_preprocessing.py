from typing import Tuple

import numpy as np
import pandas as pd
from scipy.sparse._csr import csr_matrix
from sklearn.feature_extraction import DictVectorizer

MIN_DURATION = 1
MAX_DURATION = 60
CATEGORICAL_COLS = ["PULocationID", "DOLocationID"]


def filter_outliers(
    taxi_rides: pd.DataFrame,
    min_duration: int = MIN_DURATION,
    max_duration: int = MAX_DURATION,
) -> pd.DataFrame:
    """Filter out outliers based on the ride duration.

    Args:
        taxi_rides (pd.DataFrame): DataFrame containing taxi rides.
        min_duration (int, optional): Minimum duration for a ride to be considered.
            Defaults to MIN_DURATION.
        max_duration (int, optional): Maximum duration for a ride to be considered.
            Defaults to MAX_DURATION.

    Returns:
        pd.DataFrame: DataFrame with outliers filtered out.
    """
    filtered_taxi_rides = taxi_rides.loc[
        (taxi_rides.duration >= min_duration) & (taxi_rides.duration <= max_duration)
    ]

    return filtered_taxi_rides


def encode_categorical_cols(taxi_rides: pd.DataFrame) -> pd.DataFrame:
    """Encode categorical columns in `taxi_rides` dataframe.

    Args:
        taxi_rides (pd.DataFrame): The dataframe containing taxi ride information.

    Returns:
        pd.DataFrame: The modified dataframe where the categorical columns are encoded.
    """
    taxi_rides.loc[:, CATEGORICAL_COLS] = (
        taxi_rides.loc[:, CATEGORICAL_COLS].fillna(-1).astype("int").astype("str")
    )

    return taxi_rides


def vectorize_dataframe(
    taxi_rides: pd.DataFrame, dict_vectorizer: DictVectorizer = None
) -> Tuple[csr_matrix, np.ndarray, DictVectorizer]:
    """Convert a DataFrame into a sparse matrix and target array, optionally using a pre-fit dictionary.

    Args:
        taxi_rides (pd.DataFrame): DataFrame to be converted.
        dict_vectorizer (DictVectorizer, optional): The DictVectorizer to use. Defaults to None.

    Returns:
        Tuple[csr_matrix, np.ndarray, DictVectorizer]: Tuple containing the sparse matrix representation of the
        DataFrame, the target array, and the DictVectorizer used to perform the conversion.
    """

    dicts = taxi_rides[CATEGORICAL_COLS].to_dict(orient="records")

    if dict_vectorizer is None:
        dict_vectorizer = DictVectorizer()
        dict_vectorizer.fit(dicts)
    features = dict_vectorizer.transform(dicts)
    target = taxi_rides["duration"].values

    return features, target, dict_vectorizer
