import cv2
import mediapipe as mp
import math
import numpy as np

# Hàm tính góc giữa 3 điểm
def calculate_angle(a, b, c):
    # a, b, c là các điểm (x, y) của các khớp
    radian = math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
    angle = abs(radian * 180.0 / math.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

# Khởi tạo MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Khởi tạo webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Đọc ảnh và chuyển sang RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    # Nếu có phát hiện người
    if results.pose_landmarks:
        # Vẽ các điểm keypoints lên khung hình
        mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Lấy các điểm của khớp
        landmarks = results.pose_landmarks.landmark

        # Các điểm quan trọng cho động tác giơ tay
        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y]
        elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y]
        wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y]

        # Tính góc giữa vai, khuỷu tay và cổ tay
        angle_left = calculate_angle(shoulder, elbow, wrist)

        # Kiểm tra động tác giơ tay hai bên (góc gần 90 độ)
        if 80 <= angle_left <= 100:
            cv2.putText(frame, 'Left Arm: Correct - Outward', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, 'Left Arm: Incorrect - Outward', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        # Kiểm tra động tác giơ tay trước mặt (góc gần 0 độ)
        if angle_left < 20:
            cv2.putText(frame, 'Left Arm: Correct - Forward', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, 'Left Arm: Incorrect - Forward', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        # Tương tự cho tay phải
        shoulder_right = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y]
        elbow_right = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y]
        wrist_right = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y]

        # Tính góc tay phải
        angle_right = calculate_angle(shoulder_right, elbow_right, wrist_right)

        # Kiểm tra động tác giơ tay hai bên cho tay phải
        if 80 <= angle_right <= 100:
            cv2.putText(frame, 'Right Arm: Correct - Outward', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, 'Right Arm: Incorrect - Outward', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        # Kiểm tra động tác giơ tay trước mặt cho tay phải
        if angle_right < 20:
            cv2.putText(frame, 'Right Arm: Correct - Forward', (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, 'Right Arm: Incorrect - Forward', (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Hiển thị kết quả
    cv2.imshow('Arm Pose Evaluation', frame)

    # Thoát khi nhấn phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng và đóng cửa sổ
cap.release()
cv2.destroyAllWindows()
