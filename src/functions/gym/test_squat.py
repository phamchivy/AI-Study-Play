import cv2
import mediapipe as mp
import math
import queue

# Hàm tính góc giữa 3 điểm
def calculate_angle(a, b, c):
    radian = math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
    angle = abs(radian * 180.0 / math.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

# Hàm xử lý squat
def evaluate_squat_pose(cap, frame_queue):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y]

            angle = calculate_angle(hip, knee, ankle)
            status = "Correct" if 90 <= angle <= 140 else "Incorrect"

            cv2.putText(frame, f'Angle: {int(angle)}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f'Squat: {status}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if status == "Correct" else (0, 0, 255), 2, cv2.LINE_AA)

        # Đưa khung hình vào hàng đợi
        frame_queue.put(frame)

    cap.release()
