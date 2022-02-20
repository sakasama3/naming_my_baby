import pathlib
import re
import requests
from bs4 import BeautifulSoup


def main():
    # 赤ちゃん名づけサイトの最初のページを取得する
    # response = requests.get(
    #    "https://namae-yurai.net/suitableNamaeResult.htm?character=&wordCount=0&sex=0&genre=1&myoji=%E6%A6%8A%E9%96%93&yomi="
    # )
    # soup = BeautifulSoup(response.content, "lxml")
    soup = BeautifulSoup(
        pathlib.Path("raw_result.html").read_text(encoding="utf-8"), "lxml"
    )
    myoji = "榊間"
    table_list = soup.find_all("table", class_="simple")
    for table in table_list:
        for tr in table.find_all("tr"):
            # tr.th を無視する
            if not tr.td:
                continue

            name, ruby, soukaku, tenkaku, jinkaku, chikaku = "", "", "", "", "", ""
            for td in tr.find_all("td"):
                td_text = str(td.get_text()).replace("\n", "")
                if match := re.match(r"(?P<name>.+)\((?P<ruby>.+)\)", td_text):
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

            print(f"{name=} {ruby=} {soukaku=} {tenkaku=} {jinkaku=} {chikaku=}")


if __name__ == "__main__":
    main()
