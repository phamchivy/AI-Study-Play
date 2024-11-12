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
pygame.display.set_caption("Countdown Timer with MediaPipe Capture")

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

# Hàm để lấy dữ liệu landmarks từ MediaPipe
def capture_landmarks(frame):
    # Chuyển ảnh từ BGR (OpenCV) sang RGB (MediaPipe)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Xử lý ảnh với MediaPipe Pose
    results = pose.process(rgb_frame)
    
    landmarks = {}
    if results.pose_landmarks:
        for i, landmark in enumerate(results.pose_landmarks.landmark):
            landmarks[f'landmark_{i}'] = {'x': landmark.x, 'y': landmark.y, 'z': landmark.z}
    return landmarks

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
    # Mở webcam
    cap = cv2.VideoCapture(0)

    running = True
    while running:
        ret, frame = cap.read()
        if not ret:
            break

        # Chuyển ảnh từ BGR sang RGB cho Pygame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = pygame.surfarray.make_surface(frame)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    # Khi nhấn phím 'S', đếm ngược 3 giây
                    countdown_timer(3)

                    # Sau khi đếm ngược xong, chụp và lưu dữ liệu
                    landmarks_data = capture_landmarks(frame)
                    save_to_json(landmarks_data)
                    print("Data saved to landmarks_data.json")

        # Làm mới màn hình
        screen.fill(WHITE)
        draw_button()
        screen.blit(frame, (0, 0))
        pygame.display.update()

    # Giải phóng tài nguyên
    cap.release()
    pygame.quit()

if __name__ == "__main__":
    main()
