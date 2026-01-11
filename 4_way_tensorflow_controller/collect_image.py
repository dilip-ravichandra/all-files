# collect_image.py

import cv2
import numpy as np
import os
import mediapipe as mp
from datetime import datetime

# Define labels and folder paths
LABELS = {'u': 'up', 'd': 'down', 'l': 'left', 'r': 'right'}
SAVE_DIR = 'data'

# Create folders if they don't exist
for label in LABELS.values():
    folder_path = os.path.join(SAVE_DIR, label)
    os.makedirs(folder_path, exist_ok=True)

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(0)

print("Press 'u' (up), 'd' (down), 'l' (left), 'r' (right) to collect samples.")
print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    image = cv2.flip(frame, 1)  # Mirror image
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = hands.process(image_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Collect Hand Signs", image)
    key = cv2.waitKey(10)

    if key == ord('q'):
        break

    elif key != -1 and chr(key).lower() in LABELS and result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand.landmark]).flatten()

        label = LABELS[chr(key)]
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename = os.path.join(SAVE_DIR, label, f"{label}_{timestamp}.npy")

        np.save(filename, landmarks)
        print(f"Saved {label} sample to {filename}")

cap.release()
cv2.destroyAllWindows()
