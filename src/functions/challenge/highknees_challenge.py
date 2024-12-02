import cv2
import mediapipe as mp
import time
import sqlite3  # Thêm thư viện sqlite3 nếu chưa có
from datetime import datetime
import os
import pygame
from utils.background import*
from utils.text import *
from utils.title import *
from utils.button import Button

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
font_path="../assets/fonts/Gamefont.ttf"
text_path="../assets/fonts/Text.ttf"
title_font = pygame.font.Font(font_path, 40)
back_font = pygame.font.Font(font_path, 30)
text_font=pygame.font.Font(text_path, 20)

# Màu sắc
NAVY = (25, 25, 112)
LIGHT_PINK = (255, 182, 193)
HOVER= (245, 162, 173)

start_button=Button("Start", 50, 500, 100, 50, LIGHT_PINK, HOVER)
back_button = Button("Back", 650, 500, 100, 50, LIGHT_PINK, HOVER)

# Tạo đối tượng Title
instruction_title = Title(
    text="Detail instruction:", 
    font=title_font, 
    color=LIGHT_PINK, 
    position=(SCREEN_WIDTH // 4.5, 70), 
    glow=True, 
    glow_color=(255, 223, 0), 
    glow_radius=15
)

# Nội dung hướng dẫn
instructions = [
    "Thử thách High Knees challenge, người chơi thực hiện chạy nâng cao đùi trong 30s, kết quả số reps sẽ được lưu trong High Score.",
    "Hãy tham gia thử thách với những người bạn nữa nhé!"
]

# Khởi tạo MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Hàm để kiểm tra vị trí gối
def is_high_knee(knee_y, hip_y):
    return knee_y < hip_y

def save_result_to_db(user_id, user_name, high_knee_count):
    # Xác định đường dẫn cơ sở dữ liệu
    db_path = os.path.join(os.path.dirname(__file__), "../../db/fitness_app.db")
    db_path = os.path.abspath(db_path)

    # Kiểm tra tệp tồn tại
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found: {db_path}")

    # Kết nối tới cơ sở dữ liệu
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Lấy thời gian hiện tại
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Chèn dữ liệu vào bảng
    cursor.execute("""
        INSERT INTO high_knees_results (user_id, user_name, reps, challenge_date)
        VALUES (?, ?, ?, ?)
    """, (user_id, user_name, high_knee_count, timestamp))

    # Lưu thay đổi và đóng kết nối
    conn.commit()
    conn.close()
    print("Kết quả đã được lưu vào cơ sở dữ liệu.")

def process_high_knees(image, pose, left_knee_up, right_knee_up, high_knee_count):
    results = pose.process(image)
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # Tọa độ của hông và gối
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP].y
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].y

        # Kiểm tra nếu gối trái hoặc gối phải được nâng lên
        if is_high_knee(left_knee, left_hip) and not left_knee_up:
            high_knee_count += 1
            left_knee_up = True
        elif not is_high_knee(left_knee, left_hip):
            left_knee_up = False

        if is_high_knee(right_knee, right_hip) and not right_knee_up:
            high_knee_count += 1
            right_knee_up = True
        elif not is_high_knee(right_knee, right_hip):
            right_knee_up = False

    return left_knee_up, right_knee_up, high_knee_count

def high_knees_challenge(screen):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to access camera")
        return

    duration = 31  # Thời gian thử thách (giây)
    start_time = None
    high_knee_count = 0
    left_knee_up = False
    right_knee_up = False

    # Tải hình ảnh
    image_path = "C:/Python code/Motion tracking/assets/images/highknees.png"  # Thay thế bằng đường dẫn tới hình ảnh của bạn
    image = pygame.image.load(image_path)

    # Lấy kích thước hình ảnh
    image = pygame.transform.scale(image, (280, 280))  # Thay đổi kích thước nếu cần

    running = True
    challenge_active = False  # Trạng thái thử thách

    while running:
        draw_gradient(screen, (173, 216, 230), (255, 240, 245))
        y_pos = 60
        instruction_title.draw(screen)
        show_text(screen, y_pos, instructions, SCREEN_WIDTH)
        screen.blit(image, (260, 250))
        start_button.is_hovered()
        start_button.draw(screen, back_font)
        back_button.is_hovered()
        back_button.draw(screen, back_font)

        # Cập nhật màn hình Pygame
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if back_button.is_clicked(event):
                running = False
            if start_button.is_clicked(event) and not challenge_active:
                # Đếm ngược 3 giây
                for countdown in range(3, 0, -1):
                    ret, frame = cap.read()
                    if not ret:
                        print("Error: Unable to read frame from camera")
                        running = False
                        break

                    # Hiển thị số đếm ngược trên màn hình
                    frame = cv2.flip(frame, 1)  # Lật khung hình để hiển thị như gương
                    cv2.putText(frame, f'Starting in: {countdown}s', 
                                (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3, cv2.LINE_AA)
                    cv2.imshow('High Knees Challenge', frame)

                    # Chờ 1 giây trước khi hiển thị số tiếp theo
                    if cv2.waitKey(1000) & 0xFF == ord('q'):
                        running = False
                        break
                challenge_active = True
                start_time = time.time()
        if challenge_active:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            if not ret:
                print("Error: Unable to read frame from camera")
                break

            # Xử lý logic OpenCV
            elapsed_time = time.time() - start_time
            remaining_time = max(0, int(duration - elapsed_time))

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            left_knee_up, right_knee_up, high_knee_count = process_high_knees(
                rgb_frame, pose, left_knee_up, right_knee_up, high_knee_count
            )

            # Hiển thị thông tin
            cv2.putText(frame, f'High Knees: {high_knee_count}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f'Time Left: {remaining_time}s', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            if elapsed_time >= duration:
                cv2.putText(frame, "Challenge Over!", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow('High Knees Challenge', frame)
                cv2.waitKey(3000)
                challenge_active = False

                # Yêu cầu nhập thông tin và lưu kết quả
                user_id = input("Enter your User ID: ")
                user_name = input("Enter your User Name: ")
                save_result_to_db(user_id, user_name, high_knee_count)
                print(f"Result saved for User ID {user_id}, User Name {user_name}: {high_knee_count} reps")

            cv2.imshow('High Knees Challenge', frame)

            # Nhấn 'q' để thoát
            if cv2.waitKey(1) & 0xFF == ord('q'):
                running = False

    cap.release()
    cv2.destroyAllWindows()
