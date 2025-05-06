import os
import cv2
import numpy as np
import tensorflow as tf

# 1. Đường dẫn dataset
base_dir = "dataset"

# 2. Load và tiền xử lý ảnh
def load_data(base_dir):
    images, labels = [], []
    for label in range(10):
        folder = os.path.join(base_dir, str(label))
        for fname in os.listdir(folder):
            if not fname.lower().endswith(('.png','.jpg','.jpeg')):
                continue
            path = os.path.join(folder, fname)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, (28, 28))
            img = img.astype("float32") / 255.0
            images.append(img)
            labels.append(label)
    X = np.array(images)
    y = np.array(labels)
    X = X.reshape(-1, 28, 28, 1)  # cho CNN
    y = tf.keras.utils.to_categorical(y, num_classes=10)
    return X, y

print("Loading data...")
X, y = load_data(base_dir)
print(f"Total samples: {X.shape[0]}")

# 3. Tự chia train/val (80/20) bằng NumPy
np.random.seed(42)
indices = np.arange(X.shape[0])
np.random.shuffle(indices)

split_at = int(0.8 * len(indices))
train_idx, val_idx = indices[:split_at], indices[split_at:]

X_train, X_val = X[train_idx], X[val_idx]
y_train, y_val = y[train_idx], y[val_idx]

print(f"Train samples: {len(X_train)}, Val samples: {len(X_val)}")

# 4. Xây mô hình CNN
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28,28,1)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
model.summary()

# 5. Huấn luyện
history = model.fit(
    X_train, y_train,
    epochs=10,
    batch_size=32,
    validation_data=(X_val, y_val),
    verbose=2
)

# 6. Đánh giá
val_loss, val_acc = model.evaluate(X_val, y_val, verbose=0)
print(f"Validation accuracy: {val_acc*100:.2f}%")

# 7. Lưu model
model.save("my_custom_digit_model.h5")
print("Model saved to my_custom_digit_model.h5")
