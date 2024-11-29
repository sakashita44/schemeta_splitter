import unittest
import pandas as pd
from schemeta_splitter.io import read_file, write_file, check_df_format


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

        # ワイド形式のテスト
        with open("test_wide.csv", "w") as f:
            f.write(wide_data)
        meta_df, data_df = read_file("test_wide.csv", is_wide_format=True)
        self.assertEqual(meta_df.shape, (4, 4))
        self.assertEqual(data_df.shape, (4, 3))

        # ロング形式のテスト
        with open("test_long.csv", "w") as f:
            f.write(long_data)
        meta_df, data_df = read_file("test_long.csv", is_wide_format=False)
        self.assertEqual(meta_df.shape, (4, 4))
        self.assertEqual(data_df.shape, (4, 4))

    def test_write_file(self):
        # テスト用のデータを作成
        meta_data = {
            "uid": [1, 2, 3, 4],
            "main_id": ["X", "X", "Y", "Y"],
            "sub_id": [1, 2, 1, 2],
            "group": ["A", "B", "A", "B"],
        }
        data_data = {
            "uid": [1, 2, 3, 4],
            "data1": [100, 110, 120, 130],
            "data2": [101, 110, 121, 131],
        }
        meta_df = pd.DataFrame(meta_data)
        data_df = pd.DataFrame(data_data)

        # ワイド形式のテスト
        write_file("test_output_wide.csv", meta_df, data_df, is_wide_format=True)
        written_df = pd.read_csv("test_output_wide.csv")
        self.assertEqual(written_df.shape, (4, 6))

        # ロング形式のテスト
        write_file("test_output_long.csv", meta_df, data_df, is_wide_format=False)
        written_df = pd.read_csv("test_output_long.csv", header=None)
        self.assertEqual(written_df.shape, (6, 5))

    def test_check_df_format(self):
        # テスト用のデータを作成
        meta_data = {
            "uid": [1, 2, 3, 4],
            "main_id": ["X", "X", "Y", "Y"],
            "sub_id": [1, 2, 1, 2],
            "group": ["A", "B", "A", "B"],
        }
        data_data = {
            "uid": [1, 2, 3, 4],
            "data1": [100, 110, 120, 130],
            "data2": [101, 110, 121, 131],
        }
        meta_df = pd.DataFrame(meta_data)
        data_df = pd.DataFrame(data_data)

        # メタデータのフォーマットチェック
        self.assertTrue(check_df_format(meta_df, meta=True))

        # データのフォーマットチェック
        self.assertTrue(check_df_format(data_df, meta=False))


if __name__ == "__main__":
    unittest.main()
