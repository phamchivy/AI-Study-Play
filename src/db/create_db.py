import sqlite3

# Tạo kết nối đến SQLite database (file sẽ được tạo nếu chưa tồn tại)
conn = sqlite3.connect("AI_Study_Play.db")
cursor = conn.cursor()

# Tạo bảng để lưu số lần reps
cursor.execute("""
CREATE TABLE IF NOT EXISTS handwriting_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    scores INTEGER NOT NULL,
    start_time TIMESTAMP,
    end_time TIMESTAMP
)
""")

# Tạo bảng để lưu số lần reps
cursor.execute("""
CREATE TABLE IF NOT EXISTS fingercounting_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    scores INTEGER NOT NULL,
    start_time TIMESTAMP,
    end_time TIMESTAMP
)
""")
conn.commit()
conn.close()
