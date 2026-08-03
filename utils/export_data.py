import os
import pandas as pd

# Project root is always one level above this file (utils/), regardless of
# which directory a notebook or script is run from.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def export_as_csv(dataframe, folder_name, file_name):
    """
    Exports a pandas DataFrame as a CSV file to a specified folder.

    Parameters:
        dataframe (pd.DataFrame): The DataFrame to export.
        folder_name (str): Name of the folder where CSV file will be saved.
        file_name (str): Name of the CSV file. Must end with '.csv' extension.

    Returns:
        None

    Raises:
        TypeError: If input is not a pandas DataFrame.
        ValueError: If file_name does not end with '.csv' extension.
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")
    if not file_name.lower().endswith(".csv"):
        raise ValueError("File name must end with '.csv' extension")

    folder_path = os.path.join(PROJECT_ROOT, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, file_name)

    dataframe.to_csv(file_path, index=False)
    print(f"Successfully exported the DataFrame as '{file_name}'")


def export_as_parquet(dataframe, folder_name, file_name):
    """
    Exports a pandas DataFrame as a Parquet file to a specified folder.

    Parameters:
        dataframe (pd.DataFrame): The DataFrame to export.
        folder_name (str): Name of the folder where Parquet file will be saved.
        file_name (str): Name of the Parquet file. Must end with '.parquet' extension.

    Returns:
        None

    Raises:
        TypeError: If input is not a pandas DataFrame.
        ValueError: If file_name does not end with '.parquet' extension.
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")
    if not file_name.lower().endswith(".parquet"):
        raise ValueError("File name must end with '.parquet' extension")

    folder_path = os.path.join(PROJECT_ROOT, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, file_name)

    dataframe.to_parquet(file_path, engine="pyarrow", index=False)
    print(f"Successfully exported the DataFrame as '{file_name}'")
