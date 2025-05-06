# predict.py

import cv2
import numpy as np
import tensorflow as tf

# Tải mô hình đã huấn luyện
model = tf.keras.models.load_model("functions/train_model/my_custom_digit_model.h5")

# Hàm dự đoán chữ số từ canvas
def predict_digit(canvas_image):
    gray = cv2.cvtColor(canvas_image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return 0

    # Sắp xếp contour từ trái sang phải (theo x)
    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])
    digits = ""

    for cnt in contours:
        x, y, w_box, h_box = cv2.boundingRect(cnt)
        if w_box < 5 or h_box < 5:
            continue  # bỏ qua noise nhỏ

        roi = thresh[y:y+h_box, x:x+w_box]

        # Làm nét và tăng cường ảnh
        blurred = cv2.GaussianBlur(roi, (3, 3), 0)
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]], dtype=np.float32)
        sharpened = cv2.filter2D(blurred, -1, kernel)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(sharpened)

        # Resize + pad 28x28
        digit_img = cv2.resize(enhanced, (20, 20), interpolation=cv2.INTER_AREA)
        final = np.zeros((28, 28), np.uint8)
        offset = (28 - 20) // 2
        final[offset:offset + 20, offset:offset + 20] = digit_img

        # Chuẩn bị input cho model
        final = final.astype('float32') / 255.0
        final = final.reshape(1, 28, 28, 1)

        # Dự đoán chữ số
        prediction = model.predict(final)
        digit_pred = np.argmax(prediction)
        digits += str(digit_pred)

    return digits if digits else 0