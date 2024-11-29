import pandas as pd
from typing import Tuple


def read_file(
    file_path: str, is_wide_format: bool, delimiter: str = ",", encoding: str = "utf-8"
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(file_path, delimiter=delimiter, encoding=encoding)
    if is_wide_format:
        meta_columns = df.columns[:4]
        meta_df = df[meta_columns]
        data_df = df.drop(columns=meta_columns[1:])
    else:
        meta_df = df.iloc[:4].T
        meta_df.columns = meta_df.iloc[0]
        meta_df = meta_df.drop(0)
        data_df = df.iloc[4:].T
        data_df.columns = data_df.iloc[0]
        data_df = data_df.drop(0)
    return meta_df, data_df


def write_file(
    file_path: str,
    meta_df: pd.DataFrame,
    data_df: pd.DataFrame,
    is_wide_format: bool,
    delimiter: str = ",",
    encoding: str = "utf-8",
) -> None:
    if is_wide_format:
        df = pd.concat([meta_df, data_df.drop(columns=data_df.columns[0])], axis=1)
    else:
        meta_df = meta_df.T
        data_df = data_df.T
        df = pd.concat([meta_df, data_df], axis=0)
    df.to_csv(file_path, sep=delimiter, encoding=encoding, index=False)


def check_df_format(df: pd.DataFrame, meta=True) -> bool:
    if meta:
        required_columns = set(df.columns[:4])
    else:
        required_columns = set(df.columns[1:])
    return required_columns.issubset(df.columns)
