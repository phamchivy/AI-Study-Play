import cv2
import mediapipe as mp
import math
import numpy as np
import pygame
from utils.background import *
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
    text="Deadlift instruction:", 
    font=title_font, 
    color=LIGHT_PINK, 
    position=(SCREEN_WIDTH // 4.5, 70), 
    glow=True, 
    glow_color=(255, 223, 0), 
    glow_radius=15
)

# Nội dung hướng dẫn
instructions = [
    "Deadlift chuẩn là khi lưng thẳng, vai hướng lên trên, kết hợp sức mạnh toàn bộ thân người để nâng tạ lên đến khi tạ nằm ở giữa đùi trên. Sau khi giữ tạ trong 2 - 3 giây, bắt đầu từ từ hạ tạ xuống và cảm nhận độ căng của cơ. Hạ tạ cho đến khi thanh tạ chạm sàn, nhưng thực hiện chậm và chắc chắn.",
    "Cách sử dụng: Màn hình hiển thị các yêu cầu, người dùng thực hiện và thay đổi theo yêu cầu đó.",
    "Vị trí đứng: Đứng vị trí sao cho camera quan sát được cả thân người."
]

# Hàm tính góc giữa 3 điểm
def calculate_angle(a, b, c):
    radian = math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
    angle = abs(radian * 180.0 / math.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

# Hàm kiểm tra điểm gần trên một đường thẳng
def is_aligned(a, b, c, threshold=0.05):
    slope_ac = (c[1] - a[1]) / (c[0] - a[0]) if c[0] != a[0] else float('inf')
    intercept_ac = a[1] - slope_ac * a[0]
    expected_y = slope_ac * b[0] + intercept_ac
    return abs(expected_y - b[1]) < threshold

# Khởi tạo MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def evaluate_deadlift_pose():
    cap = cv2.VideoCapture(0)
    exited = False  # Cờ đánh dấu đã thoát
    deadlift_down = False
    deadlift_count=0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)

        # Đọc ảnh và chuyển sang RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        # Nếu có phát hiện người
        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            landmarks = results.pose_landmarks.landmark

            # Các điểm quan trọng cho Deadlift: vai (11), hông (23), đầu gối (25), mắt cá (27)
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y]
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y]

            # Tính góc giữa vai, hông và đầu gối
            angle = calculate_angle(shoulder, hip, knee)

            # Tính góc giữa hông, đầu gối và mắt cá
            knee_angle = calculate_angle(hip, knee, ankle)

            # Hiển thị góc lên màn hình
            cv2.putText(frame, f'Angle: {int(angle)}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f'Knee Angle: {int(knee_angle)}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            
            # Kiểm tra thẳng lưng (góc 160-180)
            if 160 <= angle <= 180 and deadlift_down:
                deadlift_down=False
                deadlift_count+=1
                cv2.putText(frame, 'Deadlift: Correct - Lift it Down!', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Kiểm tra nếu mắt cá, đầu gối và vai gần thẳng hàng
            elif is_aligned(ankle, knee, shoulder, threshold=0.1):
                cv2.putText(frame, 'Deadlift: Good - Keep going!', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                if 90 <= angle <= 120 and knee_angle >= 120:
                    deadlift_down=True
                    cv2.putText(frame, 'Deadlift: Correct - Lift it Up (Good Form)!', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            cv2.putText(frame, f'Count: {deadlift_count}', (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Hiển thị kết quả
        cv2.imshow('Deadlift Pose Evaluation', frame)

        # Thoát khi nhấn phím 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exited = True  # Đặt cờ thoát khi nhấn 'q'
            break

    # Giải phóng và đóng cửa sổ
    cap.release()
    cv2.destroyAllWindows()
    return exited  # Trả về trạng thái thoát

def show_deadlift(screen):
    running = True
    while running:

        draw_gradient(screen, (173, 216, 230), (255, 240, 245))
        y_pos = 60
        instruction_title.draw(screen)
        show_text(screen, y_pos, instructions, SCREEN_WIDTH)
        start_button.is_hovered()
        start_button.draw(screen, back_font)
        back_button.is_hovered()
        back_button.draw(screen, back_font)

        # Cập nhật màn hình Pygame
        pygame.display.flip()
        challenge_active= False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if back_button.is_clicked(event):
                running = False
            if start_button.is_clicked(event) and not challenge_active:
                challenge_active = True
        if challenge_active:
            evaluate_deadlift_pose()

