"""
Topicのファイルを元にDBへデータを格納する
格納するデータは, page_name, en(ja)_url, en(ja)_text
"""

import psycopg2
import wikipediaapi
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# 英語版へ接続
wiki_wiki = wikipediaapi.Wikipedia(
    language="en", extract_format=wikipediaapi.ExtractFormat.WIKI
)


# DB接続情報
DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "postgres"
DB_PASS = "postgres"
DB_NAME = "wikipedia_featured_articles"


def main():
    create_DB(DB_NAME)
    os.chdir("Topic2")
    listdir = os.listdir()

    for fileName in listdir:
        fname = os.path.splitext(fileName)
        table_name = fname[0]
        table_name = table_name.replace("-", "_")
        create_table(DB_NAME, table_name)
        with open(fileName, "r", encoding="utf-8") as f:
            try:
                contents = f.readlines()
                for article in contents:
                    article = article.split("\n")
                    article = article[0]
                    page_py = wiki_wiki.page(article)
                    if page_py.exists():
                        en_url = page_py.fullurl
                        en_text = page_py.text
                        try:
                            langlink = page_py.langlinks
                            ja = langlink["ja"]
                            ja_url = ja.fullurl
                            ja_text = ja.text
                        except:
                            ja_url = "null"
                            ja_text = "null"
                        # エラー避け
                        article = article.replace("'", "''")
                        en_text = en_text.replace("'", "''")
                        ja_text = ja_text.replace("'", "''")

                        insert_into_data(
                            DB_NAME,
                            table_name,
                            article,
                            en_url,
                            en_text,
                            ja_url,
                            ja_text
                        )
            except:
                print(f"An exception occurred in {fileName}.")
            finally:
                print(fileName + ":Done")

# DBを作成
def create_DB(DB_NAME):
    conn = None
    try:
        conn = psycopg2.connect(user="postgres", password="postgres")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE {DB_NAME};")

        cur.close()
    except psycopg2.DatabaseError as error:
        print(error)
    finally:
        if conn is None:
            conn.close()

# DB接続関数
def get_connection(DB_NAME):
    return psycopg2.connect(
        "postgresql://{user}:{password}@{host}:{port}/{dbname}".format(
            user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT, dbname=DB_NAME
        )
    )


# テーブルを作成
def create_table(DB_name, table_name):
    try:
        with get_connection(DB_name) as conn:
            with conn.cursor() as cur:
                # テーブルを作成する SQL を準備

                # en_docvec, ja_docbecを後で追加
                sql = f"""
                    CREATE TABLE {table_name} (
                        page_id serial PRIMARY KEY,
                        page_name TEXT,
                        en_url TEXT,
                        en_text TEXT,
                        en_docvec FLOAT[],
                        ja_url TEXT,
                        ja_text TEXT,
                        ja_docvec FLOAT[]
                    )
                    """
                # SQL を実行し、テーブル作成
                cur.execute(sql)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_into_data(DB_name, table_name, page_name, en_url, en_text, ja_url, ja_text):
    try:
        with get_connection(DB_name) as conn:
            with conn.cursor() as cur:
                # DBにデータを保存
                # SQL実行（tbl_sampleから全データを取得）
                sql = f"""
                        INSERT INTO {table_name} (page_name, en_url, en_text, ja_url, ja_text)
                        VALUES ('{page_name}', '{en_url}','{en_text}','{ja_url}', '{ja_text}');
                        """
                cur.execute(sql)
                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


if __name__ == "__main__":
    main()
