import sqlite3
import os

# Hàm lấy high scores từ cơ sở dữ liệu
def fetch_hand_high_scores():
    # Đường dẫn đến cơ sở dữ liệu
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "AI_Study_Play.db"))
    
    # Kiểm tra nếu file database không tồn tại
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found: {db_path}")

    # Kết nối đến cơ sở dữ liệu
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Truy vấn để lấy top 10 người chơi có điểm cao nhất từ bảng handwriting_results
    cursor.execute("""
    SELECT user_name, scores FROM handwriting_results 
    ORDER BY scores DESC LIMIT 10
    """)
    
    # Lấy kết quả từ database
    scores = cursor.fetchall()

    # Đóng kết nối
    conn.close()

    return scores

# Hàm lấy high scores từ cơ sở dữ liệu
def fetch_finger_high_scores():
    # Đường dẫn đến cơ sở dữ liệu
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "AI_Study_Play.db"))
    
    # Kiểm tra nếu file database không tồn tại
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found: {db_path}")

    # Kết nối đến cơ sở dữ liệu
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Truy vấn để lấy top 10 người chơi có điểm cao nhất từ bảng handwriting_results
    cursor.execute("""
    SELECT user_name, scores FROM fingercounting_results 
    ORDER BY scores DESC LIMIT 10
    """)
    
    # Lấy kết quả từ database
    scores = cursor.fetchall()

    # Đóng kết nối
    conn.close()

    return scores
