# train_model.py

import os
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

DATA_DIR = "data"
LABELS = ['up', 'down', 'left', 'right']
MODEL_PATH = os.path.join("model", "hand_sign_model.h5")

# Load data
X, y = [], []
for idx, label in enumerate(LABELS):
    label_dir = os.path.join(DATA_DIR, label)
    for file in os.listdir(label_dir):
        if file.endswith(".npy"):
            data = np.load(os.path.join(label_dir, file))
            X.append(data)
            y.append(idx)

X = np.array(X)
y = to_categorical(y, num_classes=len(LABELS))

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build model
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(63,)),  # 21 landmarks × 3 (x, y, z)
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(4, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train model
model.fit(X_train, y_train, epochs=25, validation_data=(X_test, y_test), batch_size=16)

# Save model
os.makedirs("model", exist_ok=True)
model.save(MODEL_PATH)
print(f"✅ Model saved to {MODEL_PATH}")
