import cv2
import numpy as np
import mediapipe as mp
import time

# Khởi tạo MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

def count_fingers(hand_landmarks):
    tip_ids = [4, 8, 12, 16, 20]
    fingers = 0

    # Ngón cái
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers += 1

    # Các ngón còn lại
    for tip_id in tip_ids[1:]:
        if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y:
            fingers += 1

    return fingers

def detect_finger_count():
    cap = cv2.VideoCapture(0)
    canvas = None
    drawn_digits = ""

    hands = mp_hands.Hands(
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )

    print("===== HƯỚNG DẪN =====")
    print("Giữ tay trong khung hình 3 giây để lưu kết quả")
    print("=====================\n")

    start_time = None
    counting_started = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        if canvas is None:
            canvas = np.zeros_like(frame)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        total_fingers = 0

        if result.multi_hand_landmarks:
            if not counting_started:
                start_time = time.time()
                counting_started = True

            total_fingers = 0
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                fingers = count_fingers(hand_landmarks)
                total_fingers += fingers

            total_fingers = min(total_fingers, 10)
            cv2.putText(frame, f"Number of fingers: {total_fingers}", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

            # Đếm ngược
            elapsed = time.time() - start_time
            remaining = int(max(0, 3 - elapsed))
            if remaining > 0:
                cv2.putText(frame, f"Hold it in: {remaining}s", (10, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 0), 3)

            # Kiểm tra nếu đủ 3 giây liên tục
            if elapsed >= 3:
                drawn_digits += str(total_fingers)
                print(f"Đã phát hiện liên tục 3 giây: {total_fingers} --> Tổng: {drawn_digits}")
                break
        else:
            counting_started = False
            start_time = None
            cv2.putText(frame, "No hand detected", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

        combo = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)
        cv2.imshow("Finger Counter", combo)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    return drawn_digits