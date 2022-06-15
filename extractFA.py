"""
wiki_freatured_articlesを整理して, TopicList.txtへ書きこむ
書き込んだものをTopicへテキストファイルとしてまとめる
"""
import codecs
import os

os.mkdir('Topic')
with open("wiki_feature_articles.txt", "r", encoding="utf-8", errors="ignore") as r:
    with codecs.open("TopicList.txt", "w", encoding="utf-8") as w: # utf-8で書き込む
        content = r.readlines()
        for line in content:
            if line[0] == "=":
                line = line.strip("=")
                line = line.split("=")
                line = line[0].strip()
                w.write(line + "\n")

                print(line)
                fileName = "Topic\\" + line + ".txt"
                print(fileName)
                f = codecs.open(fileName, "w", encoding='utf-8')

            elif line[:21] == "* {{FA/BeenOnMainPage":
                line = line.split("[[")
                line = line[1].split("]]")
                f.write(line[0] + "\n")
