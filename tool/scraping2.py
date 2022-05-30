import datetime
import json
import csv
from time import sleep
import unicodedata
import pandas as pd
import requests
from requests.exceptions import Timeout
from requests.exceptions import ConnectionError
import re
import os
from tqdm import tqdm


class SyllabusTool:
    # イニシャライザ
    def __init__(self) -> None:
        self.move_to_tool()
        self.year = "2022"
        self.error = 0
        self.df_dict_list = list()
        self.path = "./timetable/" + self.year + "/csv/"
        self.file_list = self.get_files(self.path)
        self.csv_list = list()

    # もしカレントディレクトリが./toolでないなら、./toolディレクトリに移動する
    def move_to_tool(self):
        if os.path.basename(os.getcwd()) != "tool":
            os.chdir("./tool")

    # csvのファイル名一覧を取得
    def get_files(self, path: str):
        file_list = [file for file in os.listdir(
            path) if file.endswith(".csv")]
        file_list.sort()
        return file_list

    # 入力ファイルは一行で","区切りの文字列を想定
    def get_numbers(self, filepath: str):
        numbers_duplicate_check = list()
        with open(filepath, "r") as fp:
            numbers = fp.readline().strip().split(",")  # strip()は改行コード除去用
        numbers = list(set(numbers) - set(numbers_duplicate_check))  # 重複削除
        numbers_duplicate_check.extend(numbers)
        numbers.sort()
        numbers_duplicate_check.sort()
        return numbers


    # requests get
    def get_requests(self, url: str):
        try:
            res = self.response(url)
        except (Timeout, ConnectionError):
            print("\nError url:" + url)
            sleep(3)
            res = self.response(url)

        return res

    def response(self, url):
        res = requests.get(url, timeout=9.0).text
        res = unicodedata.normalize("NFKC", res)
        res = res.replace(",", "、")

        return res

    # スクレイピングし、dataframeをリストに変換
    def scraping(self, number: str):
        df_list = list()
        url = "https://www.portal.oit.ac.jp/CAMJWEB/slbssbdr.do?value(risyunen)=" + \
            self.year + "&value(semekikn)=1&value(kougicd)=" + \
            number + "&value(crclumcd)=10201200"

        try:
            dfs = pd.read_html(self.get_requests(url), encoding="utf-8")
        except (Timeout, ConnectionError):
            print("\nError numbering:" + number)
            sleep(3)
            dfs = pd.read_html(self.get_requests(url), encoding="utf-8")

        if len(dfs) > 2:
            for i in range(1, len(dfs)):
                if i == 1:
                    df = (dfs[i]).dropna(how="all").dropna(
                        how="all", axis=1).drop(dfs[1].columns[0], axis=1).drop(dfs[1].index[4])
                else:
                    df = (dfs[i]).dropna(how="all").dropna(how="all", axis=1)
                df_text = ((df.to_csv(index=False, header=False, encoding="utf-8")
                            ).replace("\u3000", ""))
                df_line = df_text.splitlines()
                df_list.append(df_line)

        return df_list, url

    def convert(self, df_list: list, number: str, csv: str, url: str) -> dict:
        value_list = list()
        jyugyo_list = list()
        jyugyo_value_list = list()
        jyugyo_key_list = list()
        hosei = 0
        text = "\n".join(df_list[1])
        key_list = ["kougi", "kougien", "nenji", "tani", "kikan", "tantousya", "numbering",
                    "gakka", "link", "nerai", "cs", "spiral", "mokuhyou", "hyoukahouhou",
                    "hyoukakijyun", "kyoukasyo", "sankousyo", "kokoroe", "officehours", "jissen"]

        # 講義名等
        for i in range(len(df_list[0])):
            value_list.append(df_list[0][i])
        value_list[2] = (str(value_list[2]).replace("年次", ""))  # 年次を削除
        value_list[5] = (re.sub("\(.+?\)", "", value_list[5])
                         ).replace("  ", " ")  # 担当者名のよみがな削除
        value_list.append(number)  # 講義コード追加
        value_list.append(csv[0])  # 学科名追加
        value_list.append(url)  # URL追加

        # 授業のねらい・概要
        value_list.append(df_list[2][0])

        # CSコース
        if "CSコース" in text:
            spiral = re.search(r"CSコース,(.*)", text).group(1)
            if len(spiral) > 0:
                value_list.append(spiral)
                hosei += 1  # 参照のズレを補正
            else:
                value_list.append("記載なし")
        else:
            value_list.append("記載なし")

        # スパイラル型教育
        if "スパイラル型教育" in text:
            spiral = re.search(r"スパイラル型教育,(.*)", text).group(1)
            if len(spiral) > 0:
                value_list.append(spiral)
                hosei += 1
            else:
                value_list.append("記載なし")
        else:
            value_list.append("記載なし")

        # 授業計画
        for i in range(1, (len(df_list[3+hosei]))):
            jyugyo_list.append(str(df_list[3+hosei][i]).split(","))  # ","で分割
        for i in range(len(jyugyo_list)):
            # テーマ
            if len(jyugyo_list[i][1]) > 0:
                jyugyo_key_list.append("theme"+str(i+1))
                jyugyo_value_list.append(jyugyo_list[i][1])
            # 内容・方法等
            if len(jyugyo_list[i][2]) > 0:
                jyugyo_key_list.append("naiyou"+str(i+1))
                jyugyo_value_list.append(jyugyo_list[i][2])
            # 予習/復習
            if len(jyugyo_list[i][3]) > 0:
                jyugyo_key_list.append("yosyu"+str(i+1))
                jyugyo_value_list.append(jyugyo_list[i][3])

        # 目標、評価方法、評価基準
        for i in range(3):
            value_list.append(df_list[(4+i)+hosei][0])

        # 教科書
        if "教科書" in text:
            kyoukasyo = re.search(r"教科書,(.*)", text).group(1)
            if len(kyoukasyo) > 0:
                value_list.append(
                    (re.search(r"出版社名(.*)", text).group(1)).replace("  ", ""))
                hosei += 1  # 参照のズレを補正
            else:
                value_list.append("記載なし")
        else:
            value_list.append("記載なし")

        # 参考書
        if "参考書" in text:
            sankousyo = re.search(r"参考書,(.*)", text).group(1)
            if len(sankousyo) > 0:
                value_list.append(
                    (re.search(r"出版社名(.*)", text).group(1)).replace("  ", ""))
                hosei += 1
            else:
                value_list.append("記載なし")
        else:
            value_list.append("記載なし")

        # 受講心得
        value_list.append(df_list[7+hosei][0])

        # オフィスアワー
        value_list.append(df_list[8+hosei][0])

        # 実践的教育
        if len(df_list[9+hosei]) > 0:
            value_list.append(df_list[9+hosei][0])
        else:
            value_list.append("記載なし")

        # 正規化と"の削除
        for i in range(len(value_list)):
            value_list[i] = unicodedata.normalize("NFKC", str(
                value_list[i])).replace("\"", "")
        for i in range(len(jyugyo_value_list)):
            jyugyo_value_list[i] = unicodedata.normalize(
                "NFKC", str(jyugyo_value_list[i])).replace("\"", "")

        # 辞書に変換
        df_dict = dict(zip(key_list, value_list))
        jyugyo_dict = dict(zip(jyugyo_key_list, jyugyo_value_list))
        if jyugyo_list != []:
            df_dict.update(jyugyo_dict)
        else:
            df_dict.update(
                {"theme1": "記載なし", "naiyou1": "記載なし", "yosyu1": "記載なし"})

        return df_dict

    # 講義名、年次、期間、担当者、単位数が全て重複してる場合、ナンバリングに追記ようにする
    def duplicate_check(self, check_df_dict: list, number: str):
        for i in range(len(self.df_dict_list)):
            df_dict = self.df_dict_list[i]
            if df_dict["kougi"] == check_df_dict["kougi"] and \
                    df_dict["nenji"] == check_df_dict["nenji"] and \
                    df_dict["kikan"] == check_df_dict["kikan"] and \
                    df_dict["tantousya"] == check_df_dict["tantousya"] and \
                    df_dict["tani"] == check_df_dict["tani"]:
                for df_dict_number in self.df_dict_list[i]["numbering"].split(" "):
                    if df_dict_number == number:
                        return False
                self.df_dict_list[i]["numbering"] += " " + number
                return False
        return True

    # 辞書をリストに追加
    def add_to_list(self, df_dict, number):
        if self.duplicate_check(df_dict, number):
            self.df_dict_list.append(df_dict)

    # jsonファイルで出力
    def save_json(self):
        with open("../web/src/data/" + self.year + ".json", "w", encoding="utf-8") as fp:
            json.dump(self.df_dict_list, fp, ensure_ascii=False, indent=4)

    # 一覧表示用のjsonファイルを作成
    def save_json_mini(self):
        dic_list = list()
        for i in range(len(self.df_dict_list)):
            # 内包表記で必要な値を抽出
            dic = {k: v for k, v in self.df_dict_list[i].items()
                   if k in {"kougi", "nenji", "kikan", "tantousya", "tani", "numbering", "gakka", "link"}}
            dic_list.append(dic)
        with open("../web/src/data/" + self.year + "mini.json", "w", encoding="utf-8") as fp:
            json.dump(dic_list, fp, ensure_ascii=False, indent=4)

    # csvファイルでも出力
    def save_csv(self):
        for df_dict in self.df_dict_list:
            self.csv_list.append(df_dict.values())
        with open("../web/src/data/" + self.year + ".csv", "w", encoding="utf-8") as fp:
            writer = csv.writer(fp, lineterminator="\n")
            writer.writerows(self.csv_list)

    def rewrite_readme(self):
        date = datetime.datetime.now(datetime.timezone(
            datetime.timedelta(hours=+9))).strftime("%Y/%m/%d")
        with open("../README.md", "r", encoding="utf-8") as fp:
            s = re.sub("\d{4}/\d{2}/\d{2}", date, fp.read())  # 更新日の書き換え
            s = re.sub("<!-- エラー数=\d{1,4} -->",
                       "<!-- エラー数=" + str(self.error) + " -->", s)  # エラー数の書き換え
        with open("../README.md", "w", encoding="utf-8") as fp:
            fp.write(s)

    def main(self):
        for file in tqdm(self.file_list, desc="全体の進捗率"):
            numbers = self.get_numbers(self.path + file)
            for number in tqdm(numbers, desc=file):
                df_list, url = self.scraping(number)
                if len(df_list) < 6:  # エラー処理
                    self.error += 1
                    continue
                df_dict = self.convert(df_list, number, file, url)  # 辞書に変換
                self.add_to_list(df_dict, number)  # 辞書をリストに追加

        # 全部含みのjsonを保存
        self.save_json()

        # 一覧表示用のjsonを保存
        self.save_json_mini()

        # 全部含みのcsvを保存
        self.save_csv()

        # READMEの書き換え
        self.rewrite_readme()


if __name__ == "__main__":
    SyllabusTool().main()
