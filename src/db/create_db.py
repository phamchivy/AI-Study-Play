import sqlite3

# Tạo kết nối đến SQLite database (file sẽ được tạo nếu chưa tồn tại)
conn = sqlite3.connect("fitness_app.db")
cursor = conn.cursor()

# Tạo bảng để lưu số lần reps
cursor.execute("""
CREATE TABLE IF NOT EXISTS high_knees_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    user_name TEXT,
    reps INTEGER NOT NULL,
    challenge_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()
conn.close()
