import cv2
import mediapipe as mp
import json
import time

# Khởi tạo MediaPipe pose và opencv
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Hàm để lấy landmarks từ frame
def get_landmarks_from_frame(frame):
    # Chuyển đổi frame sang RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Xử lý với MediaPipe Pose
    results = pose.process(rgb_frame)

    # Lấy landmarks nếu có kết quả
    if results.pose_landmarks:
        landmarks = []
        for id, lm in enumerate(results.pose_landmarks.landmark):
            landmarks.append({
                "id": id,
                "x": lm.x,
                "y": lm.y,
                "z": lm.z
            })
        return landmarks, results  # Trả về cả landmarks và results
    return None, None

# Hàm để lưu landmarks vào file JSON
def save_landmarks_to_json(landmarks, exercise_name):
    # Đặt tên file theo bài tập
    filename = f"{exercise_name}_landmarks.json"
    
    # Chuẩn bị dữ liệu
    data = {
        "exercise_name": exercise_name,
        "landmarks": landmarks
    }

    # Lưu dữ liệu vào file JSON
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Landmarks for '{exercise_name}' saved to {filename}.")

# Mở camera và lấy bộ landmarks chuẩn
cap = cv2.VideoCapture(0)

exercise_name = input("Enter the name of the exercise (e.g., squat, jumping_jack): ")

print("Press 's' to start 3-second countdown to save landmarks, or 'q' to quit.")
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Lấy landmarks và results từ frame hiện tại
    landmarks, results = get_landmarks_from_frame(frame)

    # Hiển thị khung hình và vẽ các landmarks lên khung nếu có
    if results:  # Chỉ vẽ khi có kết quả
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    cv2.imshow("Capture Landmarks", frame)

    # Nhấn 's' để bắt đầu đếm ngược và lưu landmarks vào JSON
    if cv2.waitKey(10) & 0xFF == ord('s') and landmarks:
        # Đếm ngược 3 giây
        for i in range(3, 0, -1):
            ret, frame = cap.read()
            if not ret:
                break

            # Hiển thị số đếm ngược trên màn hình
            cv2.putText(frame, str(i), (int(frame.shape[1] / 2), int(frame.shape[0] / 2)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5, cv2.LINE_AA)
            cv2.imshow("Capture Landmarks", frame)
            cv2.waitKey(1000)  # Dừng 1 giây cho mỗi số đếm ngược

        # Sau khi đếm ngược xong, lưu landmarks vào JSON
        save_landmarks_to_json(landmarks, exercise_name)
        break  # Thoát sau khi lưu xong
    
    # Nhấn 'q' để thoát mà không lưu
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
