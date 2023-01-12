# Naming My Baby

## 特徴

[赤ちゃん名づけ](https://namae-yurai.net/suitableNamaeResult.htm) のサイトの検索結果をスクレイピングし、
CSV に出力するツールです。

## 事前準備

- [Python3 のインストール](https://www.dsp.co.jp/tocreator/engineer/tips-engineer/python_installation/)
- [Poetry のインストール](https://python-poetry.org/docs/#installation)

## 実行方法

- 本サイトをローカルに git clone
- `poetry install --no-root`
- `poetry run python3 main.py [苗字] {"男","女"}`
  - 例： `poetry run python main.py 田中 男`
- result.csv が同一フォルダにできるので確認する
  - 上記の例の実行結果は [result.csv](result.csv) を確認してください

## 注意点

[赤ちゃん名づけの利用規約](https://namae-yurai.net/terms.htm) にはスクレイピング禁止とは記載されていませんが、本ツールを複数個立ち上げて実行するとサイトへの負荷が高まりますのでおやめください。
