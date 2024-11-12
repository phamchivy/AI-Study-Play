import pygame
import cv2
import mediapipe as mp
import json
import time

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Capture Landmarks with Countdown")

# Màu sắc
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Tạo nút bấm
button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100)  # Nút nằm giữa màn hình

# Khởi tạo MediaPipe pose và opencv
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Hàm để lấy landmarks từ frame
def get_landmarks_from_frame(frame):
    # Chuyển đổi frame sang RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Xử lý với MediaPipe Pose
    results = pose.process(rgb_frame)

    # Lấy landmarks nếu có kết quả
    if results.pose_landmarks:
        landmarks = []
        for id, lm in enumerate(results.pose_landmarks.landmark):
            landmarks.append({
                "id": id,
                "x": lm.x,
                "y": lm.y,
                "z": lm.z
            })
        return landmarks, results  # Trả về cả landmarks và results
    return None, None

# Hàm để lưu landmarks vào file JSON
def save_landmarks_to_json(landmarks, exercise_name):
    # Đặt tên file theo bài tập
    filename = f"{exercise_name}_landmarks.json"
    
    # Chuẩn bị dữ liệu
    data = {
        "exercise_name": exercise_name,
        "landmarks": landmarks
    }

    # Lưu dữ liệu vào file JSON
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Landmarks for '{exercise_name}' saved to {filename}.")

# Hàm để vẽ nút bấm trên màn hình
def draw_button():
    pygame.draw.rect(screen, RED, button_rect)
    font = pygame.font.SysFont('Arial', 30)
    text = font.render("Press 'S' to Start", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

# Hàm đếm ngược 3 giây
def countdown_timer():
    for i in range(3, 0, -1):
        ret, frame = cap.read()
        if not ret:
            break

        # Hiển thị số đếm ngược trên màn hình
        font = pygame.font.SysFont('Arial', 100)
        countdown_text = font.render(str(i), True, RED)
        screen.fill(WHITE)
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - countdown_text.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(1000)  # Dừng 1 giây cho mỗi số đếm ngược

# Mở camera
cap = cv2.VideoCapture(0)

# Hàm chính
def main():
    running = True
    countdown_started = False
    exercise_name = input("Enter the name of the exercise (e.g., squat, jumping_jack): ")

    while running:
        screen.fill(WHITE)
        draw_button()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and not countdown_started:
                    # Khi nhấn 'S', đếm ngược 3 giây
                    countdown_started = True
                    countdown_timer()

                    # Sau khi đếm ngược xong, chụp và lấy dữ liệu từ camera
                    while cap.isOpened():
                        ret, frame = cap.read()
                        if not ret:
                            break

                        landmarks, results = get_landmarks_from_frame(frame)

                        if landmarks:
                            save_landmarks_to_json(landmarks, exercise_name)
                            print("Landmarks saved!")
                            break  # Dừng sau khi lưu landmarks

        pygame.display.update()

    # Giải phóng tài nguyên
    cap.release()
    pygame.quit()

if __name__ == "__main__":
    main()
