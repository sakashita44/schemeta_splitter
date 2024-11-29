
import pandas as pd
from typing import Tuple

def read_file(file_path: str, is_wide_format: bool, delimiter: str = ',', encoding: str = 'utf-8') -> Tuple[pd.DataFrame, pd.DataFrame]:
    # ...existing code...

def write_file(file_path: str, meta_df: pd.DataFrame, data_df: pd.DataFrame, is_wide_format: bool, delimiter: str = ',', encoding: str = 'utf-8') -> None:
    # ...existing code...

def check_df_format(df: pd.DataFrame, meta=True) -> bool:
    # ...existing code...
