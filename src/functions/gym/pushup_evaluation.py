import cv2
import mediapipe as mp
import math

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
            if angle < 90:  # Giai đoạn xuống
                stage = 'down'
                if 70 <= angle <= 90:  # Điều kiện xuống đúng kỹ thuật
                    cv2.putText(frame, 'Push-up Down: Correct', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                else:
                    cv2.putText(frame, 'Push-up Down: Incorrect', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            elif angle > 160 and stage == 'down':  # Giai đoạn lên
                stage = 'up'
                if angle > 170:  # Điều kiện lên đúng kỹ thuật
                    cv2.putText(frame, 'Push-up Up: Correct', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    pushup_count += 1  # Tăng số lần chống đẩy khi hoàn thành một chu kỳ xuống - lên
                else:
                    cv2.putText(frame, 'Push-up Up: Incorrect', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            # Hiển thị số lần chống đẩy lên màn hình
            cv2.putText(frame, f'Count: {pushup_count}', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Hiển thị kết quả
        cv2.imshow('Push-up Pose Evaluation', frame)

        # Thoát khi nhấn phím 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Giải phóng và đóng cửa sổ
    cap.release()
    cv2.destroyAllWindows()

# Gọi hàm để chạy đánh giá động tác chống đẩy
#evaluate_pushup_pose()
