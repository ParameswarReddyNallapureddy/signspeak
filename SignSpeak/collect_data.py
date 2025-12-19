import cv2
import mediapipe as mp
import numpy as np
import os

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

label = "No"        # Change this for each gesture
samples_needed = 50

data_dir = "dataset"
save_path = os.path.join(data_dir, label)
os.makedirs(save_path, exist_ok=True)

cap = cv2.VideoCapture(0)

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
    count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

                landmarks = []
                for lm in hand.landmark:
                    landmarks.extend([lm.x, lm.y])

                cv2.putText(frame, "Press SPACE to Save",
                            (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

                key = cv2.waitKey(1)
                if key == 32 and count < samples_needed:  # SPACE key
                    np.savetxt(f"{save_path}/{count}.txt", landmarks)
                    count += 1
                    print("Saved:", count)

        cv2.putText(frame, f"Collecting: {label} ({count}/{samples_needed})",
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0), 2)

        cv2.imshow("Data Collection", frame)

        if count >= samples_needed:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
