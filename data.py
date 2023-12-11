# 地名データの前処理
import re, pickle
import pandas as pd

# データを読み込み
with open("alternateNamesV2.txt", encoding="utf-8") as f:
    lines = [line for line in f.readlines()]

# 英語と日本語のデータを抽出
english = [s for s in lines if "\ten\t" in s]
japanese = [s for s in lines if "\tja\t" in s]

# データの数チェック
print(len(lines))
print(len(english))
print(len(japanese))

# インデックスと地名をリストに出力
ja_index = []
ja_name = []
en_index = []
en_name = []

for s in japanese:
    word_bag = s.split()
    ja_index.append(word_bag[1])
    ja_name.append(word_bag[3])

for s in english:
    word_bag = s.split()
    en_index.append(word_bag[1])
    name = ""
    for i in range(3, len(word_bag)):
        name += word_bag[i] + " "
    name = re.sub(r"[0-9]", "", name)
    name = name.strip()
    en_name.append(name)

# Dataframe化
df_en = pd.DataFrame(list(zip(en_index, en_name)), columns=["code", "en_name"])
df_ja = pd.DataFrame(list(zip(ja_index, ja_name)), columns=["code", "ja_name"])

# 日本語と英語ともあるデータの抽出
df_place = pd.merge(df_ja, df_en, on="code")
# print(df_ja.info())
# print(df_en.info())
print(df_place.info())

# 辞書型に変換
ja_place = df_place["ja_name"].values.tolist()
en_place = df_place["en_name"].values.tolist()
dict_place = {ja_place[i]: en_place[i] for i in range(len(ja_place))}

print(len(dict_place))

# 一時保存
with open('dict_place.pkl', 'wb') as f:
    pickle.dump(dict_place, f)

# 読み込み
# with open('dict_place.pkl', 'rb') as f:
#     dict_place = pickle.load(f)
#
# try:
#     city = dict_place["a"]
# except KeyError:
#     city = "null"
#
# print(city)

