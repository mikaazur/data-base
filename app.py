import os
import sqlite3

# データベース接続関数
def connect_db():
    db_path = os.path.join(os.path.dirname(__file__), "movie_db.db")
    return sqlite3.connect(db_path)

# 映画を検索する関数
def search_movies(keyword):
    conn = connect_db()
    cur = conn.cursor()
    query = "SELECT * FROM movies WHERE title LIKE ? OR genre LIKE ?;"
    cur.execute(query, ('%' + keyword + '%', '%' + keyword + '%'))
    movies = cur.fetchall()
    cur.close()
    conn.close()
    return movies

# 映画のレビューを追加する関数
def add_review(movie_id, user_name, rating, review_text):
    conn = connect_db()
    cur = conn.cursor()
    # 映画が存在するか確認
    cur.execute("SELECT * FROM movies WHERE movie_id = ?", (movie_id,))
    movie = cur.fetchone()
    if not movie:
        raise ValueError("指定された映画IDは存在しません。")
    # レビューを追加
    query = """
        INSERT INTO reviews (movie_id, user_name, rating, review_text)
        VALUES (?, ?, ?, ?);
    """
    cur.execute(query, (movie_id, user_name, rating, review_text))
    conn.commit()
    cur.close()
    conn.close()

# 映画のレビューを取得する関数
def get_reviews(movie_id):
    conn = connect_db()
    cur = conn.cursor()
    # 映画が存在するか確認
    cur.execute("SELECT * FROM movies WHERE movie_id = ?", (movie_id,))
    movie = cur.fetchone()
    if not movie:
        raise ValueError("指定された映画IDは存在しません。")
    # レビューを取得
    query = """
        SELECT user_name, rating, review_text, review_date
        FROM reviews
        WHERE movie_id = ?;
    """
    cur.execute(query, (movie_id,))
    reviews = cur.fetchall()
    cur.close()
    conn.close()
    return reviews

# メインメニュー
def main():
    while True:
        print("\n--- 映画データベース ---")
        print("1. 映画を検索")
        print("2. 映画のレビューを投稿")
        print("3. 映画のレビューを見る")
        print("4. 終了")
        choice = input("選択してください: ")

        if choice == "1":
            keyword = input("検索キーワードを入力: ")
            if not keyword.strip():  # 空の入力チェック
                print("キーワードを入力してください。")
                continue
            movies = search_movies(keyword)
            if movies:
                for movie in movies:
                    print(f"ID: {movie[0]}, タイトル: {movie[1]}, ジャンル: {movie[2]}, 年: {movie[3]}")
            else:
                print("該当する映画が見つかりませんでした。")
        
        elif choice == "2":
            try:
                movie_id = int(input("レビューする映画のIDを入力: "))
                if movie_id <= 0:
                    raise ValueError("映画IDは正の整数でなければなりません。")
                user_name = input("ユーザー名を入力: ")
                if not user_name.strip():  # 空のユーザー名チェック
                    raise ValueError("ユーザー名を入力してください。")
                rating = int(input("評価を1～5で入力: "))
                if rating < 1 or rating > 5:
                    raise ValueError("評価は1～5の範囲で入力してください。")
                review_text = input("レビュー内容を入力: ")
                add_review(movie_id, user_name, rating, review_text)
                print("レビューが投稿されました！")
            except ValueError as e:
                print(f"エラー: {e}")

        elif choice == "3":
            try:
                movie_id_input = input("レビューを表示する映画のIDを入力: ")
                if not movie_id_input.strip():  # 空の入力チェック
                    print("映画IDを入力してください。")
                    continue
                movie_id = int(movie_id_input)
                reviews = get_reviews(movie_id)
                if reviews:
                    for review in reviews:
                        print(f"ユーザー: {review[0]}, 評価: {review[1]}, レビュー: {review[2]}, 投稿日: {review[3]}")
                else:
                    print("レビューがありません。")
            except ValueError as e:
                print(f"エラー: {e}")

        elif choice == "4":
            print("終了します。")
            break

        else:
            print("無効な選択です。もう一度選択してください。")

if __name__ == "__main__":
    main()
