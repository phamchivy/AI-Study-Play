import pygame
import random
import cv2
import mediapipe as mp
import time
import math
from utils.background import *
from utils.button import Button


# Các động tác cần nhận diện theo thứ tự
GESTURES = ["Trai tim", "Gio 2 ngon tay", "Hinh tron"]

# MediaPipe khởi tạo
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

# Hàm tính góc giữa hai điểm
def calculate_angle(point1, point2):
    dx = point2.x - point1.x
    dy = point2.y - point1.y
    return math.degrees(math.atan2(dy, dx))

# Tính khoảng cách giữa hai điểm
def calculate_distance(p1, p2):
    return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5

# Hàm kiểm tra động tác
def check_gesture(gesture, frame,result):
    hands_landmarks = []
    for hand_landmarks in result.multi_hand_landmarks:
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        hands_landmarks.append(hand_landmarks.landmark)

    # Nhận diện động tác
    for hand_landmarks in hands_landmarks:
    # 1. Like
        thumb_tip = hand_landmarks[mp_hands.HandLandmark.THUMB_TIP]
        thumb_ip = hand_landmarks[mp_hands.HandLandmark.THUMB_IP]
        thumb_mcp = hand_landmarks[mp_hands.HandLandmark.THUMB_CMC]
    
    # Kiểm tra hướng ngón cái và vị trí tương đối
    if thumb_tip.y < thumb_ip.y < thumb_mcp.y:  # Đầu ngón cái phải cao hơn các khớp dưới
        thumb_angle = calculate_angle(hand_landmarks[mp_hands.HandLandmark.THUMB_CMC],
                                hand_landmarks[mp_hands.HandLandmark.THUMB_TIP])
        if 85 <= abs(thumb_angle) <= 95:  # Góc vuông chặt chẽ hơn
            return True
    # 2. Xòe 5 ngón tay
    if gesture == "Xoe 5 ngon tay":
        # 2. Xòe 5 ngón tay
        extended_count = 0
        for i in range(5):
            tip = mp_hands.HandLandmark(i * 4 + 4)  # Điểm đầu ngón tay
            dip = mp_hands.HandLandmark(i * 4 + 3)  # Điểm giữa ngón tay
            pip = mp_hands.HandLandmark(i * 4 + 2)  # Điểm gần lòng bàn tay
            if hand_landmarks[tip].y < hand_landmarks[dip].y < hand_landmarks[pip].y:  # Ngón tay xòe thẳng
                extended_count += 1
        if extended_count == 5:  # Tất cả ngón tay được xòe ra đầy đủ
            return True
    # 3. Giơ 2 ngón tay
    if gesture == "Gio 2 ngon tay":
        # 3. Giơ 2 ngón tay (chữ V)
        dist_index_middle = calculate_distance(hand_landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP],
                                                hand_landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP])
        dist_index_thumb = calculate_distance(hand_landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP],
                                                hand_landmarks[mp_hands.HandLandmark.THUMB_TIP])
        dist_middle_thumb = calculate_distance(hand_landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
                                                hand_landmarks[mp_hands.HandLandmark.THUMB_TIP])

        if dist_index_middle > 0.15 and dist_index_thumb > 0.15 and dist_middle_thumb > 0.15:
            return True
    # 4. Hình tròn
    if gesture == "Hinh tron":
        thumb_tip = hand_landmarks[mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        if calculate_distance(thumb_tip, index_tip) < 0.05:
            return True
    # 5. Trái tim
    if gesture == "Trai tim":
        # 5. Hình trái tim (giảm độ chính xác)
        if len(hands_landmarks) == 2:
            left_hand = hands_landmarks[0]
            right_hand = hands_landmarks[1]

            left_thumb_tip = left_hand[mp_hands.HandLandmark.THUMB_TIP]
            right_thumb_tip = right_hand[mp_hands.HandLandmark.THUMB_TIP]
            left_index_tip = left_hand[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            right_index_tip = right_hand[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            dist_thumb = calculate_distance(left_thumb_tip, right_thumb_tip)
            dist_index = calculate_distance(left_index_tip, right_index_tip)

            # Nới lỏng các điều kiện
            if dist_thumb < 0.3 and dist_index < 0.3:  # Tăng khoảng cách được phép
                if left_index_tip.y > left_hand[mp_hands.HandLandmark.INDEX_FINGER_MCP].y and \
                right_index_tip.y > right_hand[mp_hands.HandLandmark.INDEX_FINGER_MCP].y:
                  return True  # Chỉ mang tính minh họa, bạn cần thêm logic
    return False

# Khởi tạo camera
cap = cv2.VideoCapture(0)

# Chọn động tác ngẫu nhiên
current_gesture = random.choice(GESTURES)
start_time = time.time()
score = 0
current_gesture_index = 0
current_gesture = GESTURES[current_gesture_index]

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
font_path="../assets/fonts/Gamefont.ttf"
text_path="../assets/fonts/Text.ttf"
title_font = pygame.font.Font(font_path, 50)
back_font = pygame.font.Font(font_path, 30)
text_font=pygame.font.Font(text_path, 20)

# Màu sắc
NAVY = (25, 25, 112)
LIGHT_PINK = (255, 182, 193)
HOVER= (245, 162, 173)

back_button = Button("Back", 270, 200, 100, 50, LIGHT_PINK, HOVER)

# Hàm bắt đầu trò chơi nhận diện động tác, nhận đối tượng cửa sổ Pygame từ ngoài
def start_gesture_game(screen):
    # Khởi tạo camera
    cap = cv2.VideoCapture(0)

    # Chọn động tác ban đầu
    current_gesture_index = 0
    current_gesture = GESTURES[current_gesture_index]
    start_time = time.time()
    score = 0

    # Vòng lặp chính
    running = True
    while running:
        draw_gradient(screen, (173, 216, 230), (255, 240, 245))

        back_button.is_hovered()
        back_button.draw(screen, back_font)

        gesture_text = text_font.render(f"Do this gesture: {current_gesture}", True, NAVY)
        screen.blit(gesture_text, (50, 50))
        
        # Hiển thị điểm
        score_text = text_font.render(f"Score: ", True, NAVY)
        screen.blit(score_text, (50, 100))

        # Hiển thị điểm
        score_num = title_font.render(f"{score}", True, HOVER)
        screen.blit(score_num, (150, 90))

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if back_button.is_clicked(event):
                cap.release()
                cv2.destroyAllWindows()
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                return # Trở về menu chính khi nhấn nút Back
        
        # Camera và MediaPipe
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)
        
        if result.multi_hand_landmarks:
            if check_gesture(current_gesture, frame,result):
                score += 1
                current_gesture_index = (current_gesture_index + 1) % len(GESTURES)  # Chuyển sang động tác tiếp theo
                current_gesture = GESTURES[current_gesture_index]  # Lấy động tác tiếp theo
                start_time = time.time()

        # Kiểm tra thời gian
        #if time.time() - start_time > 10:  # Quá 10 giây để thực hiện động tác
            #running = False

        # Hiển thị camera trong cửa sổ OpenCV
        cv2.imshow("Camera", frame)
        
        # Cập nhật màn hình Pygame
        pygame.display.flip()

    # Dọn dẹp
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()