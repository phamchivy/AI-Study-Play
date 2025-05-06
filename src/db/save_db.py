import os
import sqlite3

def save_handwriting_result_to_db(user_name, score, start_time, end_time):
    # Đường dẫn tới cơ sở dữ liệu
    db_path = os.path.join(os.path.dirname(__file__), "../db/AI_Study_Play.db")
    db_path = os.path.abspath(db_path)

    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found: {db_path}")

    # Kết nối tới cơ sở dữ liệu
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Chèn dữ liệu vào bảng handwriting_results
    cursor.execute("""
        INSERT INTO handwriting_results (user_name, scores, start_time, end_time)
        VALUES (?, ?, ?, ?)
    """, (user_name, score, start_time, end_time))

    conn.commit()
    conn.close()
    print("\n✅ Kết quả handwriting quiz đã được lưu.")

def save_finger_result_to_db(user_name, score, start_time, end_time):
    db_path = os.path.join(os.path.dirname(__file__), "../db/AI_Study_Play.db")
    db_path = os.path.abspath(db_path)

    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO fingercounting_results (user_name, scores, start_time, end_time)
        VALUES (?, ?, ?, ?)
    """, (user_name, score, start_time, end_time))

    conn.commit()
    conn.close()
    print("\n✅ Kết quả finger counting quiz đã được lưu.")