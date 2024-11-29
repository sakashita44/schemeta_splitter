import argparse
import os
import pandas as pd
from .io import read_file, write_file


def main():
    parser = argparse.ArgumentParser(
        description="schemeta_splitter: メタデータとデータの分割/結合ツール"
    )
    parser.add_argument("-i", "--input", required=True, help="入力ファイルのパス")
    parser.add_argument("-o", "--output", required=True, help="出力ディレクトリのパス")
    parser.add_argument(
        "-w", "--wide", action="store_true", help="ワイド形式のファイルかどうか"
    )
    parser.add.argument(
        "-d", "--delimiter", default=",", help="デリミタ (デフォルト: ,)"
    )
    parser.add.argument(
        "-e", "--encoding", default="utf-8", help="エンコーディング (デフォルト: utf-8)"
    )
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"Error: Input file {args.input} does not exist.")
        return

    if not os.path.isdir(args.output):
        print(f"Error: Output directory {args.output} does not exist.")
        return

    try:
        meta_df, data_df = read_file(
            args.input,
            is_wide_format=args.wide,
            delimiter=args.delimiter,
            encoding=args.encoding,
        )
        output_file = os.path.join(args.output, "output.csv")
        write_file(
            output_file,
            meta_df,
            data_df,
            is_wide_format=args.wide,
            delimiter=args.delimiter,
            encoding=args.encoding,
        )
        print(f"File successfully written to {output_file}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except pd.errors.EmptyDataError as e:
        print(f"No data: {e}")
    except pd.errors.ParserError as e:
        print(f"Parsing error: {e}")
    except Exception as e:
        print(f"Error processing file: {e}")


if __name__ == "__main__":
    main()
