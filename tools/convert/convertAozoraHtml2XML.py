import xml.dom.minidom
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import requests
import sys
import argparse
import re


def parse_args(args=sys.argv[1:]):
    """ Get the parsed arguments specified on this script.
    """
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        'url',
        action='store',
        type=str,
        help='Target aozora bunko url.')

    return parser.parse_args(args)


def get_dates_and_persons(text):
    # 修正作業用の辞書
    p_types = [{"ja": "入力", "en": "Aozora Transcription"}, {"ja": "校正", "en": "Aozora Proofreading"}]
    d_types = ["作成", "修正"]

    dates = []
    persons = []

    lines = text.split("<lb/>")

    for line in lines:
        line = line.strip()

        for type in p_types:
            if line.startswith(type["ja"] + "："):
                person = line.split("：")[1]
                persons.append({"type@ja": type["ja"], "name": person, "type@en": type["en"]})

        for type in d_types:
            if line.endswith("日" + type):
                date_arr = line.replace("年", "-").replace("月", "-").replace("日", "-").split("-")
                year = date_arr[0]
                month = date_arr[1].zfill(2)
                day = date_arr[2].zfill(2)

                date = year + "-" + month + "-" + day
                date_str = line.split("日")[0] + "日"

                dates.append({"org": date_str, "rep": date, "type": type})

    return dates, persons


def handle_bibliographical_information(text):
    bib_info = text
    bib_info = bib_info.split("<hr/>")[1]
    bib_info = bib_info.split("ボランティアの皆さんです。")[0] + "ボランティアの皆さんです。"
    bib_info = bib_info.replace('<a href="http://www.aozora.gr.jp/">', "")
    bib_info = bib_info.replace("</a>", "")

    bib_info = bib_info.replace("<br/>", "<lb/>")

    # 微修正
    bib_info = bib_info.replace("class=", "rend=")

    # 日時、日付情報の取得
    dates, persons = get_dates_and_persons(bib_info)

    note = '<note>%s</note>' % bib_info

    return note, dates, persons


prefix = ".//{http://www.tei-c.org/ns/1.0}"

template_path = "data/template.xml"
output_path = "data/result.xml"

tree = ET.parse(template_path)
ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
root = tree.getroot()

args = parse_args()

# HTMLの取得
r = requests.get(args.url)
soup = BeautifulSoup(r.content, "lxml")
bib_info = soup.select(".bibliographical_information")[0]

# 文字列解析により、noteの整形、および日時情報、人物情報を取得する
note, dates, persons = handle_bibliographical_information(str(bib_info))

respStmt = root.find(prefix + "respStmt")

# 取得した日時情報で、note内の日時情報を書き換える
for date in dates:
    note = note.replace(date["org"], '<date when="%s">%s</date>' % (date["rep"], date["org"]))

    if date["type"] == "作成":
        respStmt.append(ET.fromstring('<resp when="%s">作成</resp>' % date["rep"]))

respStmt.append(ET.fromstring(note))

# 人物情報の追加
titleStmt = root.find(prefix + "titleStmt")
for person in persons:
    titleStmt.append(
        ET.fromstring('<respStmt><resp>%s</resp><name>%s</name></respStmt>' % (person["type@en"], person["name"])))

titleStmt.append(
    ET.fromstring('<respStmt><resp when="2019-01-01">TEI Encoding</resp><name>Input Your Name</name></respStmt>'))

# タイトルと著者情報の追加
title = soup.select(".title")[0].text
root.find(prefix + "title").text = title
author = soup.select(".author")[0].text
root.find(prefix + "author").text = author

bibl = root.find(prefix + "bibl")
bibl.append(ET.fromstring('<title>%s</title>' % title))
bibl.append(ET.fromstring('<author>%s</author>' % author))
bibl.text = "Input by your self"

# ----------- 以下、本文 -----------

body = root.find(prefix + "body")

p = ET.Element("{http://www.tei-c.org/ns/1.0}p")
body.append(p)

main_text = soup.select(".main_text")[0]

text = str(main_text)
text = text.replace("class=", "rend=")
text = text.replace("<br/>", "<lb/>")
text = text.replace("id=", "xml:id=")
text = text.replace("src=", "facs=")
text = text.replace("img ", "span rendition='img' ")
text = text.replace("alt=", "source=")
text = text.replace("<div", "<span rendition='div'")
text = text.replace("</div>", "</span>")

text = re.sub('<h\d(.+?)<\/h\d>', '<span\\1</span>', text)
text = re.sub('<a(.+?)<\/a>', '<span\\1</span>', text)

text = re.sub('<ruby>(.+?)<\/ruby>', '<span type="ruby">\\1</span>', text)
text = re.sub('<rb>(.+?)<\/rb>', '<span type="rb">\\1</span>', text)
text = re.sub('<rp>(.+?)<\/rp>', '<span type="rp">\\1</span>', text)
text = re.sub('<rt>(.+?)<\/rt>', '<span type="rt">\\1</span>', text)

p.append(ET.fromstring(text))

# --以下、出力 --

tree.write(output_path, encoding="utf-8")

# 整形
xml = xml.dom.minidom.parse(output_path)
pretty_xml_as_string = xml.toprettyxml()

file = open(output_path, 'w')
file.write(pretty_xml_as_string)
file.close()
