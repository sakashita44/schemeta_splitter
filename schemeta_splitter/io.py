import pandas as pd
from typing import Tuple


def read_file(
    file_path: str, is_wide_format: bool, delimiter: str = ",", encoding: str = "utf-8"
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(file_path, delimiter=delimiter, encoding=encoding, index_col=0)
    if is_wide_format:
        meta_columns = df.columns[:3]
        meta_df = df[meta_columns]
        data_df = df.drop(columns=meta_columns)
    else:
        meta_df = df.iloc[:3].T
        meta_columns = df.index[:3]
        meta_df.columns = meta_columns
        index_name = meta_df.columns.name
        meta_df.columns.name = ""
        meta_df.index.name = index_name

        data_df = df.iloc[3:].T
        data_columns = df.index[3:]
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
