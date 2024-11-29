# schemeta_splitter

`schemeta_splitter`: 規程形式の(メタデータとデータが混在した)テキストファイルを，メタデータとデータのDataFrame(pandas)に分割/またはその逆を行うPythonパッケージ

## インストール

事前にgitがインストールされている必要がある

```bash
pip install git+https://github.com/sakashita44/schemeta_splitter.git
```

## 依存ライブラリ

* pandas

## 対応ファイル形式

* CSVまたはTSV形式で以下のいずれかのテーブル形式のファイル

### ワイド形式 (入力例)

* データ読み込み時にis_wide_format=Trueとする

| uid | main_id | sub_id | group | data1 | data2 | data3 | data4 | ... |
| --- | ------- | ------ | ----- | ----- | ----- | ----- | ----- | --- |
| 1   | X       | 1      | A     | 100   | 101   | 102   | 103   | ... |
| 2   | X       | 2      | B     | 110   | 110   | 111   | 112   | ... |
| 3   | Y       | 1      | A     | ...   | ...   | ...   | ...   | ... |
| 4   | Y       | 2      | B     | ...   | ...   | ...   | ...   | ... |
| 5   | X       | 3      | C     | ...   | ...   | ...   | ...   | ... |
| ... | ...     | ...    | ...   | ...   | ...   | ...   | ...   | ... |

* uid: ユニークID (同一ファイル内でのみ有効，別ファイルでは異なる値を持つ可能性あり)
* main_id: 主ID
    * 例: 被験者番号等
* sub_id: 副ID
    * 例: 試行番号等
* group: 群
    * 例: 実験における条件等 (介入群: A, 対照群: B 等)
* data1, data2, data3, data4, ...: データの値
    * 例: 実験で得られた測定値，計算されたパラメータ等

### ロング形式 (入力例)

* データ読み込み時にis_wide_format=Falseとする

| uid     | 1   | 2   | 3   | 4   | 5   | ... |
| ------- | --- | --- | --- | --- | --- | --- |
| main_id | X   | Y   | X   | Y   | X   | ... |
| sub_id  | 1   | 1   | 2   | 2   | 3   | ... |
| group   | A   | A   | B   | B   | C   | ... |
| data1   | 100 | 110 | ... | ... | ... | ... |
| data2   | 101 | 110 | ... | ... | ... | ... |
| data3   | 102 | 111 | ... | ... | ... | ... |
| data4   | 103 | 112 | ... | ... | ... | ... |
| ...     | ... | ... | ... | ... | ... | ... |

上から4行 (メタデータ行)

* uid: ユニークID (同一ファイル内でのみ有効，別ファイルでは異なる値を持つ可能性あり)
* main_id: 主ID
    * 例: 被験者番号等
* sub_id: 副ID
    * 例: 試行番号等
* group: 群
    * 例: 実験における条件等 (介入群: A, 対照群: B 等)

5行目以降 (データ行)

* 1列目: index
    * 例: 時間 (1秒, 2秒, ...) や連番 (1回目, 2回目, ...) 等の順序を表す値
* 2列目以降: 各サンプル (各被験者・試行) のデータ値
    * 例: サンプルごとの測定値や計算値の時系列データ
        * 上記の表では被験者Xの1回目試行のデータが1列目，被験者Yの1回目試行のデータが2列目，という形で並ぶ

## 分割後のデータ形式

### メタデータのDataFrame

| uid | main_id | sub_id | group |
| --- | ------- | ------ | ----- |
| 1   | X       | 1      | A     |
| 2   | X       | 2      | B     |
| 3   | Y       | 1      | A     |
| 4   | Y       | 2      | B     |
| 5   | X       | 3      | C     |
| ... | ...     | ...    | ...   |

* uidはindexとして扱われ，index名はもとのファイルの列名と同じになる
* それ以外の列の列名は元のファイルの列名と同じになる

### データのDataFrame

| uid | data1 | data2 | data3 | data4 | ... |
| --- | ----- | ----- | ----- | ----- | --- |
| 1   | 100   | 101   | 102   | 103   | ... |
| 2   | 110   | 110   | 111   | 112   | ... |
| 3   | ...   | ...   | ...   | ...   | ... |

## 使い方

### ライブラリとして使う

```python

import schemeta_splitter as ss

# ワイド形式のファイルを読み込む
meta_df, data_df = ss.read_file('input.csv', is_wide_format=True, delimiter=',', encoding='utf-8')

# ロング形式のファイルを読み込む
meta_df, data_df = ss.read_file('input.csv', is_wide_format=False, delimiter=',', encoding='utf-8')

# メタデータとデータのDataFrameをファイルに書き出す
ss.write_file('output.csv', meta_df, data_df, is_wide_format=True, delimiter=',', encoding='utf-8')

```

### コマンドラインツールとして使う

pipでインストールすると，schemeta_splitterコマンドが使えるようになる

```bash
schemeta_splitter -i input.csv -o output_dir
```

* -i: 入力ファイルのパス
* -o: 出力ディレクトリのパス
* -w: ワイド形式のファイルかどうか (True: ワイド形式, False: ロング形式)
* -d: デリミタ (デフォルト: ',')
* -e: エンコーディング (デフォルト: 'utf-8')
* -h: ヘルプ
* -v: バージョン
