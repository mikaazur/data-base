import os
import sqlite3

def setup_db():
    # .dbファイルをapp.pyと同じフォルダに作成
    db_path = os.path.join(os.path.dirname(__file__), "movie_db.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # テーブル作成
    cur.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            year INTEGER NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            review_id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER NOT NULL,
            user_name TEXT NOT NULL,
            rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
            review_text TEXT NOT NULL,
            review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(movie_id) REFERENCES movies(movie_id)
        );
    """)

    # サンプル映画データを追加
    cur.execute("INSERT OR IGNORE INTO movies (title, genre, year) VALUES ('Inception', 'Sci-Fi', 2010);")
    cur.execute("INSERT OR IGNORE INTO movies (title, genre, year) VALUES ('The Godfather', 'Crime', 1972);")
    cur.execute("INSERT OR IGNORE INTO movies (title, genre, year) VALUES ('The Dark Knight', 'Action', 2008);")

    conn.commit()
    cur.close()
    conn.close()
    print("データベースとテーブルがセットアップされました。")

if __name__ == "__main__":
    setup_db()
