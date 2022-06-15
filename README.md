# Store wikipedia_featured_articles data in DB using postgresql

前提：postgresqlの環境構築，wikipediaapi, psycopg2等のpythonライブラリの環境構築を終わらせておくこと．

## 手順の説明：
1. [wikipedia:featured articles](https://en.wikipedia.org/wiki/Wikipedia:Featured_articles)へアクセスし，ソースの内容をwiki_feature_articles.txtへコピペする
2. extractFA.pyを実行し，TopicList.txtおよびTopicフォルダとそのコンテンツを作成．
3. Add_Data_to_DB.pyを実行する．

<span style="color: red; ">DBのカラムであるen_docvec, ja_docvecが空になっているが，これに対しては別途プログラムを作成する．</span>

成功したらこんな感じになる↓
![スクリーンショット (2)](https://user-images.githubusercontent.com/74339912/173758660-088ceef7-e3c2-4fd0-937f-d6aa8f384c1c.png)
