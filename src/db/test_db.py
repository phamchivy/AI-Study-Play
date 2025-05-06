import sqlite3
from datetime import datetime

# Kết nối tới cơ sở dữ liệu
conn = sqlite3.connect("AI_Study_Play.db")
cursor = conn.cursor()

# Dữ liệu cần chèn
user_name = "Pham Chi Vy"
scores = 0
start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Chèn vào handwriting_results
cursor.execute("""
    INSERT INTO handwriting_results (user_name, scores, start_time, end_time)
    VALUES (?, ?, ?, ?)
""", (user_name, scores, start_time, end_time))

conn.commit()
print("Đã chèn vào handwriting_results.\n")

# Chèn vào fingercounting_results
cursor.execute("""
    INSERT INTO fingercounting_results (user_name, scores, start_time, end_time)
    VALUES (?, ?, ?, ?)
""", (user_name, scores, start_time, end_time))

conn.commit()
print("Đã chèn vào fingercounting_results.\n")

# Đóng kết nối
conn.close()
