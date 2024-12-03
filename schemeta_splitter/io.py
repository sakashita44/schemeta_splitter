import pandas as pd
from typing import Tuple


def read_file(
    file_path: str,
    is_wide_format: bool,
    delimiter: str = ",",
    encoding: str = "utf-8",
    metadata_count: int = 3,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Read a file and return the metadata and data as separate dataframes.

    Parameters
    ----------
    file_path : str
        The path to the file to read.
    is_wide_format : bool
        Whether the file is in wide format or not.
    delimiter : str, optional
        The delimiter used in the file, by default ",".
    encoding : str, optional
        The encoding of the file, by default "utf-8".
    metadata_count : int, optional
        The number of rows that contain metadata(exclude index col), by default 3.

    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame]
        A tuple containing the metadata and data dataframes.
            1. The metadata dataframe. (wide format)
            2. The data dataframe. (wide format)
    """

    df = pd.read_csv(file_path, delimiter=delimiter, encoding=encoding, index_col=0)
    if is_wide_format:
        meta_columns = df.columns[:metadata_count]
        meta_df = df[meta_columns]
        data_df = df.drop(columns=meta_columns)
    else:
        meta_df = df.iloc[:metadata_count].T
        meta_columns = df.index[:metadata_count]
        meta_df.columns = meta_columns
        index_name = meta_df.columns.name
        meta_df.columns.name = ""
        meta_df.index.name = index_name

        data_df = df.iloc[metadata_count:].T
        data_columns = df.index[metadata_count:]
        data_df.columns = data_columns
        data_df.index.name = index_name
        data_df.columns.name = ""
        data_df.index.name = index_name

    if len(meta_df) == 0 or len(data_df) == 0:
        raise ValueError("The number of rows in meta_df or data_df is 0.")
    if len(data_df.columns) == 0:
        raise ValueError("The number of columns in data_df is 0.")
    return meta_df, data_df


def write_file(
    file_path: str,
    meta_df: pd.DataFrame,
    data_df: pd.DataFrame,
    is_wide_format: bool,
    delimiter: str = ",",
    encoding: str = "utf-8",
) -> None:
    """
    Write the metadata and data dataframes to a file.

    Parameters
    ----------
    file_path : str
        The path to the file to write.
    meta_df : pd.DataFrame
        The metadata dataframe. (wide format)
    data_df : pd.DataFrame
        The data dataframe. (wide format)
    is_wide_format : bool
        Whether the file is in wide format or not.
    delimiter : str, optional
        The delimiter to use in the file, by default ",".
    encoding : str, optional
        The encoding of the file, by default "utf-8".
    """
    if len(meta_df) != len(data_df):
        raise ValueError("The number of rows in meta_df and data_df must be the same.")
    if is_wide_format:
        df = pd.concat([meta_df, data_df], axis=1)
        save_index = True
    else:
        index_name = meta_df.index.name
        meta_df = meta_df.T
        data_df = data_df.T
        df = pd.concat([meta_df, data_df], axis=0)
        df.index.name = index_name
        save_index = True
    df.to_csv(file_path, sep=delimiter, encoding=encoding, index=save_index)
