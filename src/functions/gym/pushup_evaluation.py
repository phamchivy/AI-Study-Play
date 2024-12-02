import cv2
import mediapipe as mp
import math
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
    text="Push up instruction:", 
    font=title_font, 
    color=LIGHT_PINK, 
    position=(SCREEN_WIDTH // 4.5, 70), 
    glow=True, 
    glow_color=(255, 223, 0), 
    glow_radius=15
)

# Nội dung hướng dẫn
instructions = [
    "Push up chuẩn là khi lưng thẳng, xuống kiểm soát đến khi khuỷu tay vuông góc và lên thẳng tay.",
    "Cách sử dụng: Màn hình hiển thị các yêu cầu, người dùng thực hiện và thay đổi theo yêu cầu đó.",
    "Vị trí đứng: Đặt camera sao cho quan sát được toàn bộ thân người."
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

def evaluate_pushup_pose():
    cap = cv2.VideoCapture(0)
    stage = None  # Trạng thái chống đẩy: 'down' hoặc 'up'
    pushup_count = 0  # Đếm số lần chống đẩy hoàn thành

    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if not ret:
            break

        # Đọc ảnh và chuyển sang RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        # Nếu có phát hiện người
        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            landmarks = results.pose_landmarks.landmark

            # Các điểm quan trọng cho chống đẩy: vai (11), khuỷu tay (13), cổ tay (15)
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y]

            # Tính góc giữa vai, khuỷu tay và cổ tay
            angle = calculate_angle(shoulder, elbow, wrist)

            # Hiển thị góc lên màn hình
            cv2.putText(frame, f'Angle: {int(angle)}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            # Đánh giá giai đoạn xuống và lên
            if 80 <= angle <= 100:  # Giai đoạn xuống
                if stage != 'down':  # Nếu trạng thái thay đổi từ "up" -> "down"
                    stage = 'down'
                    cv2.putText(frame, 'Push-up Down: Correct', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    cv2.putText(frame, f'Stage: {stage}', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                #else:
                    #cv2.putText(frame, 'Push-up Down: Incorrect', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            elif angle > 150 and stage == 'down':  # Giai đoạn lên
                stage = 'up'
                cv2.putText(frame, 'Push-up Up: Correct', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(frame, f'Stage: {stage}', (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                pushup_count += 1  # Tăng số lần chống đẩy khi hoàn thành một chu kỳ xuống - lên
                #else:
                    #cv2.putText(frame, 'Push-up Up: Incorrect', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            # Hiển thị số lần chống đẩy lên màn hình
            cv2.putText(frame, f'Count: {pushup_count}', (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Hiển thị kết quả
        cv2.imshow('Push-up Pose Evaluation', frame)

        # Thoát khi nhấn phím 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Giải phóng và đóng cửa sổ
    cap.release()
    cv2.destroyAllWindows()

def show_pushup(screen):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to access camera")
        return
    running = True
    while running:

        draw_gradient(screen, (173, 216, 230), (255, 240, 245))
        y_pos = 60
        instruction_title.draw(screen)
        show_text(screen, y_pos, instructions, SCREEN_WIDTH)
        #screen.blit(image, (260, 250))
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
                    cv2.imshow('Count down', frame)

                    # Chờ 1 giây trước khi hiển thị số tiếp theo
                    if cv2.waitKey(1000) & 0xFF == ord('q'):
                        running = False
                        break
                # Giải phóng và đóng cửa sổ
                cap.release()
                cv2.destroyAllWindows()
                challenge_active = True
        if challenge_active:
            evaluate_pushup_pose()


