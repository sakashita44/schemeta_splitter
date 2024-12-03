import os
import unittest
import pandas as pd
from schemeta_splitter.io import read_file, write_file


class TestIO(unittest.TestCase):
    def test_read_file(self):
        # テスト用のデータを作成
        wide_data = """uid,main_id,sub_id,group,data1,data2
1,X,1,A,100,101
2,X,2,B,110,110
3,Y,1,A,120,121
4,Y,2,B,130,131"""
        long_data = """uid,1,2,3,4
main_id,X,Y,X,Y
sub_id,1,1,2,2
group,A,A,B,B
data1,100,110,120,130
data2,101,110,121,131"""

        # データ保存先を作成
        os.makedirs("tests/data", exist_ok=True)

        # ワイド形式のテスト
        with open("tests/data/test_wide.csv", "w") as f:
            f.write(wide_data)
        meta_df, data_df = read_file("tests/data/test_wide.csv", is_wide_format=True)
        self.assertEqual(meta_df.shape, (4, 3))
        self.assertEqual(data_df.shape, (4, 2))

        # ロング形式のテスト
        with open("tests/data/test_long.csv", "w") as f:
            f.write(long_data)
        meta_df, data_df = read_file("tests/data/test_long.csv", is_wide_format=False)
        self.assertEqual(meta_df.shape, (4, 3))
        self.assertEqual(data_df.shape, (4, 2))

    def test_write_file(self):
        # テスト用のデータを作成
        meta_data = {
            "uid": [1, 3, 2, 4],
            "main_id": ["X", "Y", "X", "Y"],
            "sub_id": [1, 1, 2, 2],
            "group": ["A", "A", "B", "B"],
        }
        data_data = {
            "uid": [1, 2, 3, 4],
            "data1": [100, 110, 120, 130],
            "data2": [101, 110, 121, 131],
        }
        meta_df = pd.DataFrame(meta_data).set_index("uid")
        data_df = pd.DataFrame(data_data).set_index("uid")

        # データ保存先を作成
        os.makedirs("tests/data", exist_ok=True)

        # ワイド形式のテスト
        write_file(
            "tests/data/test_output_wide.csv", meta_df, data_df, is_wide_format=True
        )
        written_df = pd.read_csv("tests/data/test_output_wide.csv", index_col=0)
        self.assertEqual(written_df.shape, (4, 5))

        # ロング形式のテスト
        write_file(
            "tests/data/test_output_long.csv", meta_df, data_df, is_wide_format=False
        )
        written_df = pd.read_csv(
            "tests/data/test_output_long.csv", index_col=0, header=None
        )
        self.assertEqual(written_df.shape, (6, 4))


if __name__ == "__main__":
    unittest.main()
