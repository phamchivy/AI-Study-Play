import sqlite3

# Kết nối đến database
conn = sqlite3.connect("AI_Study_Play.db")
cursor = conn.cursor()

# Hàm hiển thị dữ liệu từ 1 bảng
def show_table_data(table_name):
    print(f"\nDữ liệu trong bảng {table_name}:")
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("Không có dữ liệu.")

# Hiển thị dữ liệu từ handwriting_results
show_table_data("handwriting_results")

# Hiển thị dữ liệu từ fingercounting_results
show_table_data("fingercounting_results")

# Đóng kết nối
conn.close()
