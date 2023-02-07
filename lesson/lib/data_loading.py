import urllib.request
from pathlib import Path
from typing import Tuple

import pandas as pd

TRAIN_DEST_PATH = "data/yellow_tripdata_2021-01.parquet"
TEST_DEST_PATH = "data/yellow_tripdata_2021-02.parquet"

TRAIN_SOURCE_URL = (
    "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"
)
TEST_SOURCE_URL = (
    "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-02.parquet"
)
PICKUP_COLUMN = "tpep_pickup_datetime"
DROPOFF_COLUMN = "tpep_dropoff_datetime"


def load_data(root_dir: Path) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load and preprocess train and test data.

    Args:
        root_dir (Path): Root directory where data should be stored.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: Tuple of train and test dataframes.

    """
    if not (root_dir / TRAIN_DEST_PATH).exists():
        urllib.request.urlretrieve(TRAIN_SOURCE_URL, root_dir / TRAIN_DEST_PATH)
    if not (root_dir / TEST_DEST_PATH).exists():
        urllib.request.urlretrieve(TEST_SOURCE_URL, root_dir / TEST_DEST_PATH)

    train_df = compute_target(pd.read_parquet(root_dir / TRAIN_DEST_PATH))
    test_df = compute_target(pd.read_parquet(root_dir / TEST_DEST_PATH))

    return train_df, test_df


def compute_target(df: pd.DataFrame) -> pd.DataFrame:
    df["duration"] = df[DROPOFF_COLUMN] - df[PICKUP_COLUMN]
    df["duration"] = df["duration"].dt.total_seconds() / 60

    return df
