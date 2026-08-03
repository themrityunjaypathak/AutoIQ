import os
import pandas as pd

# Project root is always one level above this file (utils/), regardless of
# which directory a notebook or script is run from.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_csv(folder_name, file_name):
    """
    Reads a CSV file from a specified folder and returns a DataFrame.

    Parameters:
        folder_name (str): Name of the folder containing the CSV file.
        file_name (str): Name of the CSV file, must end with .csv extension.

    Returns:
        pd.DataFrame: A DataFrame containing the contents of the CSV file.

    Raises:
        ValueError: If file_name does not end with .csv extension.
        FileNotFoundError: If folder does not exist or file does not exist in the specified folder.
    """
    if not file_name.endswith(".csv"):
        raise ValueError("File name must end with '.csv' extension")

    folder_path = os.path.join(PROJECT_ROOT, folder_name)
    file_path = os.path.join(folder_path, file_name)

    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"Folder '{folder_name}' does not exists")
    if not os.path.isfile(file_path):
        raise FileNotFoundError(
            f"File '{file_name}' not found in folder '{folder_name}'"
        )

    return pd.read_csv(file_path)


def load_parquet(folder_name, file_name):
    """
    Reads a Parquet file from a specified folder and returns a DataFrame.

    Parameters:
        folder_name (str): Name of the folder containing the Parquet file.
        file_name (str): Name of the Parquet file, must end with .parquet extension.

    Returns:
        pd.DataFrame: A DataFrame containing the contents of the Parquet file.

    Raises:
        ValueError: If file_name does not end with .parquet extension.
        FileNotFoundError: If folder does not exist or file does not exist in the specified folder.
    """
    if not file_name.endswith(".parquet"):
        raise ValueError("File name must end with '.parquet' extension")

    folder_path = os.path.join(PROJECT_ROOT, folder_name)
    file_path = os.path.join(folder_path, file_name)

    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"Folder '{folder_name}' does not exists")
    if not os.path.isfile(file_path):
        raise FileNotFoundError(
            f"File '{file_name}' not found in folder '{folder_name}'"
        )

    return pd.read_parquet(file_path, engine="pyarrow")
