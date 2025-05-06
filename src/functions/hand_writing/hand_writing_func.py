import cv2
import numpy as np
import mediapipe as mp
import time
from functions.train_model.predict import predict_digit

def get_drawn_digit():
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    hands = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )

    cap = cv2.VideoCapture(0)
    canvas = None
    prev_x, prev_y = None, None

    print("===== VẼ CHỮ SỐ TRẢ LỜI =====")
    print("Nhấn 's' để xác nhận chữ số bạn vừa vẽ.")
    print("Nhấn 'c' để xóa và vẽ lại.")
    print("Nhấn 'ESC' để thoát mà không gửi câu trả lời.")
    print("Tự động thoát sau 15 giây.")
    print("==================================")

    predicted_digit = 0
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        if canvas is None:
            canvas = np.zeros_like(frame)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            lm = result.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)

            x_tip = int(lm.landmark[8].x * w)
            y_tip = int(lm.landmark[8].y * h)

            if lm.landmark[8].y < lm.landmark[6].y:
                if prev_x is not None:
                    cv2.line(canvas, (prev_x, prev_y), (x_tip, y_tip), (255, 255, 255), 8)
                prev_x, prev_y = x_tip, y_tip
            else:
                prev_x, prev_y = None, None
        else:
            prev_x, prev_y = None, None

        combo = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)

        # === Đếm ngược 15 giây ===
        elapsed = time.time() - start_time
        remaining_time = int(max(0, 15 - elapsed))
        cv2.putText(combo, f"Time left: {remaining_time}s", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.putText(combo, "Draw a digit and press 's'", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow("Draw Digit", combo)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            predicted_digit = None
            break
        elif key == ord('s') or elapsed >= 15:
            predicted_digit = predict_digit(canvas)
            break
        elif key == ord('c'):
            canvas = np.zeros_like(frame)

    cap.release()
    cv2.destroyAllWindows()
    return predicted_digit