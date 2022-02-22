import argparse
import const
import csv
import logging
import pathlib
import re
import requests
from urllib import parse
from bs4 import BeautifulSoup
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple


def fetch_names(
    myoji: str, sex: int, genre: int = 1, page: int = 1
) -> Tuple[List[Dict[str, Any]], bool]:
    """赤ちゃん名づけサイトから名前一覧と総格・三格を取得する

    Args:
        myoji (str): 苗字
        page (int): ページ

    Returns:
        List[Dict[str, Any]]: 取得した情報の辞書のリスト
        bool: 次ページ有無
    """
    logger = logging.getLogger(__name__)
    url_encoded_myoji = parse.quote(myoji)
    url = (
        f"https://namae-yurai.net/suitableNamaeResult.htm?myoji={url_encoded_myoji}"
        f"&sex={sex}&genre={genre}&wordCount=&character=&yomi=&page={page}"
    )
    logger.debug(f"{url=}")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")

    # 名前・総格・三格の取得
    result_list = list()
    table_list = soup.find_all("table", class_="simple")
    for table in table_list:
        for tr in table.find_all("tr"):
            # tr.th を無視する
            if not tr.td:
                continue

            name, ruby, soukaku, tenkaku, jinkaku, chikaku = "", "", "", "", "", ""
            for td in tr.find_all("td"):
                td_text = str(td.get_text()).replace("\n", "")
                if match := re.match(rf"{myoji} (?P<name>.+)\((?P<ruby>.+)\)", td_text):
                    name = match.group("name")
                    ruby = match.group("ruby")

                elif match := re.match(r"総格:(?P<soukaku>\d+)", td_text):
                    soukaku = match.group("soukaku")

                elif match := re.match(
                    r"天格:(?P<tenkaku>\d+) 人格:(?P<jinkaku>\d+) 地格:(?P<chikaku>\d+)",
                    td_text,
                ):
                    tenkaku = match.group("tenkaku")
                    jinkaku = match.group("jinkaku")
                    chikaku = match.group("tenkaku")

            result_list.append(
                {
                    "ジャンル": const.GENRE_DICT[genre],
                    "ページ": page,
                    "名前": name,
                    "読み": ruby,
                    "総格": soukaku,
                    "天格": tenkaku,
                    "人格": jinkaku,
                    "地格": chikaku,
                }
            )

    # 次ページ有無
    page_links = soup.select("p a")
    for page_link in page_links:
        if page_link.get_text() == "次ページ":
            next_page_exists = True
            break
    else:
        next_page_exists = False

    return result_list, next_page_exists


def main(myoji: str, sex: str, filename: str):
    logger = logging.getLogger(__name__)

    ############################################################
    # 赤ちゃん名づけサイトの最初のページを取得する
    ############################################################
    result_list = list()
    for genre in const.GENRE_DICT.keys():
        exists_next_page = True
        page = 1
        while exists_next_page:
            logger.info(f"ジャンル: {const.GENRE_DICT[genre]}, ページ {page} 取得中")
            result_list_tmp, exists_next_page = fetch_names(
                myoji, const.SEX_DICT[sex], genre, page
            )
            logger.debug(f"{exists_next_page=}")
            result_list.extend(result_list_tmp)
            page += 1

    logger.debug(result_list)

    ############################################################
    # CSV に出力
    ############################################################
    logger.info(f"CSVファイル {filename} に出力中")
    # Windows だと空行が入ってしまうため newline="" を指定する
    with pathlib.Path(filename).open("w", encoding="utf-8", newline="") as f:
        fieldnames = result_list[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(result_list)


if __name__ == "__main__":
    # ログの設定
    logging.basicConfig(
        level=logging.INFO,
        format="{asctime} [{levelname:.4}] {name}: {message}",
        style="{",
    )

    parser = argparse.ArgumentParser("指定した名字と字画のよい名前を赤ちゃん名づけから取得して CSV に出力する")
    parser.add_argument("myoji", help="苗字")
    parser.add_argument("sex", help="性別", choices=["男", "女"])
    parser.add_argument("--csv_file_name", help="出力する CSV のファイル名", default="result.csv")
    args = parser.parse_args()
    main(args.myoji, args.sex, args.csv_file_name)
