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
    # Read the file into a DataFrame
    df = pd.read_csv(file_path, delimiter=delimiter, encoding=encoding, index_col=0)

    # Check uid duplication
    if is_wide_format:
        uids = df.index
    else:
        with open(file_path, "r", encoding=encoding) as f:
            first_line = f.readline()
        uids = first_line.strip().split(delimiter)

    if len(uids) != len(set(uids)):
        raise ValueError("The uid contains duplicates.")

    # Split the DataFrame into metadata and data
    meta_df, data_df = split_dataframe(df, is_wide_format, metadata_count)

    return meta_df, data_df


def split_dataframe(
    df: pd.DataFrame, is_wide_format: bool, metadata_count: int = 3
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split a DataFrame into metadata and data DataFrames.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to split (prescribed format).
        The prescribed format is as follows: https://github.com/sakashita44/schemeta_splitter?tab=readme-ov-file#%E5%AF%BE%E5%BF%9C%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E5%BD%A2%E5%BC%8F
    is_wide_format : bool
        Whether the DataFrame is in wide format or not.
    metadata_count : int
        The number of rows that contain metadata(exclude index col).

    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame]
        A tuple containing the metadata and data dataframes.
            1. The metadata dataframe. (wide format)
            2. The data dataframe. (wide format)
    """
    # Process the DataFrame based on the format (wide or long)
    if is_wide_format:
        # Check for duplicate indices
        if len(df.index) != len(set(df.index)):
            raise ValueError("The uid contains duplicates.")
        # Split the DataFrame into metadata and data
        meta_columns = df.columns[:metadata_count]
        meta_df = df[meta_columns]
        data_df = df.drop(columns=meta_columns)

    else:
        # Check for duplicate columns
        columns = df.columns
        if len(columns) != len(set(columns)):
            raise ValueError("The uid contain duplicates.")
        # Transpose and split the DataFrame into metadata and data
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

    # Validate the resulting DataFrames
    if len(meta_df) == 0 and metadata_count > 0:
        raise ValueError("The number of rows in meta_df is 0.")
    if len(data_df) == 0:
        raise ValueError("The number of rows in data_df is 0.")
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
        Whether the file saved in wide format or not.
    delimiter : str, optional
        The delimiter to use in the file, by default ",".
    encoding : str, optional
        The encoding of the file, by default "utf-8".
    """
    # Concatenate the metadata and data DataFrames
    df = concatenate_dataframes(meta_df, data_df, is_wide_format)
    # Write the concatenated DataFrame to a file
    df.to_csv(file_path, sep=delimiter, encoding=encoding, index=True)


def concatenate_dataframes(
    meta_df: pd.DataFrame, data_df: pd.DataFrame, get_wide_format: bool
) -> pd.DataFrame:
    """
    Concatenate the metadata and data dataframes into a selected format.

    Parameters
    ----------
    meta_df : pd.DataFrame
        The metadata dataframe. (wide format)
    data_df : pd.DataFrame
        The data dataframe. (wide format)
    get_wide_format : bool
        Whether to return the concatenated dataframe in wide format or not.

    Returns
    -------
    pd.DataFrame
        The concatenated dataframe.
    """

    # Check if the index of meta_df and data_df match
    if not set(meta_df.index) == set(data_df.index):
        raise ValueError("The index of meta_df and data_df do not match.")

    # Concatenate the DataFrames based on the format (wide or long)
    if get_wide_format:
        df = pd.concat([meta_df, data_df], axis=1)
    else:
        index_name = meta_df.index.name
        meta_df = meta_df.T
        data_df = data_df.T
        df = pd.concat([meta_df, data_df], axis=0)
        df.index.name = index_name
        df.columns.name = ""

    return df
