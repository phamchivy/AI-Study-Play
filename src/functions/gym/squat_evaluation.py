import cv2
import mediapipe as mp
import math
import numpy as np
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
    text="Squat instruction:", 
    font=title_font, 
    color=LIGHT_PINK, 
    position=(SCREEN_WIDTH // 4.5, 70), 
    glow=True, 
    glow_color=(255, 223, 0), 
    glow_radius=15
)

# Nội dung hướng dẫn
instructions = [
    "Squat chuẩn là khi lưng thẳng, xuống kiểm soát và đưa mông ra sau.",
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

# Khởi tạo MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def evaluate_squat_pose():
    cap = cv2.VideoCapture(0)
    exited = False  # Cờ đánh dấu đã thoát

    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            landmarks = results.pose_landmarks.landmark

            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y]
            angle = calculate_angle(hip, knee, ankle)

            cv2.putText(frame, f'Angle: {int(angle)}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            if 90 <= angle <= 140:
                cv2.putText(frame, 'Squat: Correct - Stand up', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                cv2.putText(frame, 'Squat: Correct - Squat down', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('Squat Pose Evaluation', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            exited = True  # Đặt cờ thoát khi nhấn 'q'
            break

    cap.release()
    cv2.destroyAllWindows()
    return exited

def show_squat(screen):
    # Tải hình ảnh
    image_path = "C:/Python code/Motion tracking/assets/images/squat.jpeg"  # Thay thế bằng đường dẫn tới hình ảnh của bạn
    image_squat = pygame.image.load(image_path)
    # Lấy kích thước hình ảnh
    image_squat = pygame.transform.scale(image_squat, (380, 190))  # Thay đổi kích thước nếu cần
    running = True
    while running:

        draw_gradient(screen, (173, 216, 230), (255, 240, 245))
        y_pos = 60
        instruction_title.draw(screen)
        show_text(screen, y_pos, instructions, SCREEN_WIDTH)
        screen.blit(image_squat, (260, 320))
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
            evaluate_squat_pose()

