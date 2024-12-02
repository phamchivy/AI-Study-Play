import sqlite3
from datetime import datetime

# Kết nối tới cơ sở dữ liệu
conn = sqlite3.connect("fitness_app.db")
cursor = conn.cursor()

# Dữ liệu cần chèn
user_id = 1
user_name = "John Doe"
high_knee_count = 25
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Câu lệnh INSERT INTO
cursor.execute("""
    INSERT INTO high_knees_results (user_id,user_name, reps, challenge_date)
    VALUES (?, ?, ?, ?)
""", (user_id,user_name, high_knee_count, timestamp))

# Lưu thay đổi vào cơ sở dữ liệu
conn.commit()

print("Dữ liệu đã được chèn vào bảng.")

# Đóng kết nối
conn.close()
