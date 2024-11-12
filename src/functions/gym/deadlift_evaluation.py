import cv2
import mediapipe as mp
import math
import numpy as np

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

def evaluate_deadlift_pose():
    cap = cv2.VideoCapture(0)
    exited = False  # Cờ đánh dấu đã thoát

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Đọc ảnh và chuyển sang RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        # Nếu có phát hiện người
        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            landmarks = results.pose_landmarks.landmark

            # Các điểm quan trọng cho Deadlift: vai (11), hông (23), đầu gối (25)
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y]
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y]

            # Tính góc giữa vai, hông và đầu gối
            angle = calculate_angle(shoulder, hip, knee)

            # Hiển thị góc lên màn hình
            cv2.putText(frame, f'Angle: {int(angle)}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Đánh giá mức độ chính xác của động tác Deadlift
            # Ví dụ: nếu góc nằm trong khoảng 160-180 độ thì đúng (phần lưng thẳng)
            if 160 <= angle <= 180:
                cv2.putText(frame, 'Deadlift: Correct', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                cv2.putText(frame, 'Deadlift: Incorrect', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

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

# Gọi hàm để chạy đánh giá động tác Deadlift
#evaluate_deadlift_pose()
