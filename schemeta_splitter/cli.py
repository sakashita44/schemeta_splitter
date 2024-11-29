
import argparse
import pandas as pd
from .io import read_file, write_file

def main():
    parser = argparse.ArgumentParser(description='schemeta_splitter: メタデータとデータの分割/結合ツール')
    parser.add_argument('-i', '--input', required=True, help='入力ファイルのパス')
    parser.add_argument('-o', '--output', required=True, help='出力ディレクトリのパス')
    parser.add_argument('-w', '--wide', action='store_true', help='ワイド形式のファイルかどうか')
    parser.add_argument('-d', '--delimiter', default=',', help='デリミタ (デフォルト: ,)')
    parser.add_argument('-e', '--encoding', default='utf-8', help='エンコーディング (デフォルト: utf-8)')
    args = parser.parse_args()

    meta_df, data_df = read_file(args.input, is_wide_format=args.wide, delimiter=args.delimiter, encoding=args.encoding)
    write_file(args.output, meta_df, data_df, is_wide_format=args.wide, delimiter=args.delimiter, encoding=args.encoding)

if __name__ == '__main__':
    main()
