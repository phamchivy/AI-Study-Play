import sqlite3

# Kết nối và lấy dữ liệu từ bảng
conn = sqlite3.connect("fitness_app.db")
cursor = conn.cursor()

# Lấy toàn bộ dữ liệu
cursor.execute("SELECT * FROM high_knees_results")
rows = cursor.fetchall()

# In ra dữ liệu
for row in rows:
    print(row)

conn.close()
