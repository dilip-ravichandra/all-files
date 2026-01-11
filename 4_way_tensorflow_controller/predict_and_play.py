import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

# Track action delay
last_action_time = 0
delay_between_actions = 1  # seconds

# Mapping from grid to key actions
grid_actions = {
    (0, 1): "up",
    (2, 1): "down",
    (1, 0): "left",
    (1, 2): "right"
}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip and convert
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame
    result = hands.process(rgb_frame)

    # Draw grid: 3x3
    for i in range(1, 3):
        cv2.line(frame, (0, i * h // 3), (w, i * h // 3), (0, 255, 0), 2)
        cv2.line(frame, (i * w // 3, 0), (i * w // 3, h), (0, 255, 0), 2)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Draw hand landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get index finger tip
            index_tip = hand_landmarks.landmark[8]
            x = int(index_tip.x * w)
            y = int(index_tip.y * h)

            # Draw fingertip
            cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)

            # Grid cell detection
            row = y // (h // 3)
            col = x // (w // 3)
            grid_cell = (row, col)

            # Perform action if in mapping
            action = grid_actions.get(grid_cell)
            current_time = time.time()
            if action and (current_time - last_action_time) > delay_between_actions:
                pyautogui.press(action)
                print(f"Action: {action}")
                last_action_time = current_time

            # Display grid cell on screen
            cv2.putText(frame, f"Grid: {grid_cell}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Show frame
    cv2.imshow("Grid-Based Control", frame)

    if cv2.waitKey(1) == ord('q'):
        break

# Release
cap.release()
cv2.destroyAllWindows()
