import cv2
import mediapipe as mp
import pickle
import pyttsx3
import time
import threading
import queue

# -----------------------------
# LOAD MODEL & INITIAL SETUP
# -----------------------------
model = pickle.load(open("model.pkl", "rb"))

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

_speech_queue = queue.Queue()


def _speech_worker():
    engine = pyttsx3.init()
    while True:
        text = _speech_queue.get()
        if text is None:
            break
        try:
            engine.say(text)
            engine.runAndWait()
        finally:
            _speech_queue.task_done()


_speech_thread = threading.Thread(target=_speech_worker, daemon=True)
_speech_thread.start()

sentence = []
paused = False

last_prediction = ""
last_add_time = 0
last_speak_time = 0

ADD_DELAY = 3.0
AUTO_SPEAK_DELAY = 3.0

SENTENCE_FILE = "current_sentence.txt"

# -----------------------------
# 🔴 VERY IMPORTANT CHANGE
# -----------------------------
cap = None   # ✅ CAMERA IS OFF BY DEFAULT


def start_camera():
    """Open camera ONLY when needed"""
    global cap
    if cap is None:
        cap = cv2.VideoCapture(0)


def stop_camera():
    """Release camera safely"""
    global cap
    if cap:
        cap.release()
        cap = None


def generate_frames():
    """
    This function is called ONLY when:
    - user clicks 'Sign → Text'
    - browser requests /video_feed
    """
    global cap, last_prediction, last_add_time, last_speak_time

    start_camera()   # ✅ Camera starts HERE (not before)

    with mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7
    ) as hands:

        while cap and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                continue

            frame = cv2.flip(frame, 1)
            now = time.time()

            if not paused:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = hands.process(rgb)

                if result.multi_hand_landmarks:
                    for hand in result.multi_hand_landmarks:
                        mp_draw.draw_landmarks(
                            frame, hand, mp_hands.HAND_CONNECTIONS
                        )

                        landmarks = []
                        for lm in hand.landmark:
                            landmarks.extend([lm.x, lm.y])

                        prediction = model.predict([landmarks])[0]

                        if prediction != last_prediction and (now - last_add_time) > ADD_DELAY:
                            sentence.append(prediction)
                            last_prediction = prediction
                            last_add_time = now

                            with open(SENTENCE_FILE, "w") as f:
                                f.write(" ".join(sentence))

            # 🔊 AUTO SPEAK (non-blocking)
            if sentence and (now - last_add_time) > AUTO_SPEAK_DELAY and (now - last_speak_time) > AUTO_SPEAK_DELAY:
                _speech_queue.put(" ".join(sentence))
                last_speak_time = now

            # DISPLAY TEXT ON FRAME
            cv2.putText(
                frame,
                "Sentence: " + " ".join(sentence),
                (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2
            )

            # SEND FRAME TO BROWSER
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
            )

    stop_camera()
