import cv2
import mediapipe as mp
import pygame
import numpy as np

# Khởi tạo Mediapipe và Pygame
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Khởi tạo Pygame
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pose Estimation with Pygame and Mediapipe")

# Khởi tạo webcam
cap = cv2.VideoCapture(0)

# Vòng lặp chính của Pygame
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Đọc frame từ webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Chuyển đổi màu của frame từ BGR (OpenCV) sang RGB (Mediapipe)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Xử lý pose estimation với Mediapipe
    results = pose.process(frame_rgb)

    # Vẽ các điểm và kết nối trên frame nếu tìm thấy pose
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame_rgb, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Chuyển đổi từ định dạng RGB (Mediapipe) sang định dạng phù hợp với Pygame (Surface)

    frame_surface = pygame.surfarray.make_surface(frame_rgb)

    # Cập nhật hiển thị trên cửa sổ Pygame
    screen.blit(pygame.transform.rotate(frame_surface, -90), (0, 0))
    pygame.display.flip()

# Giải phóng tài nguyên
cap.release()
pose.close()
pygame.quit()
