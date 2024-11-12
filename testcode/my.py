import pygame
import time
import json
import mediapipe as mp
import cv2

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

# Khởi tạo MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Hàm để hiển thị đếm ngược trên màn hình
def countdown_timer(seconds):
    for i in range(seconds, 0, -1):
        # Làm sạch màn hình
        screen.fill(WHITE)
        
        # Tạo font chữ
        font = pygame.font.SysFont('Arial', 100)
        
        # Tạo text để vẽ lên màn hình
        text = font.render(str(i), True, RED)
        
        # Vẽ text lên màn hình
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        
        # Cập nhật màn hình
        pygame.display.flip()
        
        # Chờ 1 giây
        pygame.time.delay(1000)
        
        # Kiểm tra nếu người dùng thoát
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

# Hàm để lấy dữ liệu landmarks từ MediaPipe (hoặc từ file nếu đã có sẵn)
def capture_landmarks_from_file(file_path):
    # Đây là cách đọc từ file JSON chứa landmarks (nếu có sẵn)
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        print("Landmarks loaded from file.")
        return data
    except Exception as e:
        print(f"Error loading file: {e}")
        return {}

# Hàm lưu dữ liệu vào file JSON
def save_to_json(data, filename='landmarks_data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Hàm để vẽ nút bấm trên màn hình
def draw_button():
    pygame.draw.rect(screen, RED, button_rect)
    font = pygame.font.SysFont('Arial', 30)
    text = font.render("Press 'S' to Start", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

# Hàm chính
def main():
    running = True
    countdown_started = False
    landmarks_data = {}

    while running:
        screen.fill(WHITE)
        draw_button()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and not countdown_started:
                    # Khi nhấn phím 'S', đếm ngược 3 giây
                    countdown_started = True
                    countdown_timer(3)

                    # Sau khi đếm ngược xong, chụp và lấy dữ liệu từ file landmarks của bạn
                    landmarks_data = capture_landmarks_from_file('path_to_your_landmarks_file.json')
                    
                    if landmarks_data:
                        save_to_json(landmarks_data)  # Lưu landmarks vào file JSON
                        print("Data saved to landmarks_data.json")
                    else:
                        print("No landmarks data available.")

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
