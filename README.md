### ✅ Project Name

**Malware Simulation Framework v2 — Python-Based Keylogger + Payload**

### 📄 `README.md` 
```markdown
# 🛡️ Python-Based Malware Simulation Framework (Keylogger + Payload)

> ⚠️ **Disclaimer:** This project is for **educational and ethical hacking purposes only**. It was built and tested in a **controlled environment** to understand the inner workings of malware, data exfiltration, and defensive countermeasures. Do not use this project for unauthorized access or malicious activities.

---

## 📌 Overview

This project is a **Level 2 upgrade** of my initial keylogger script, now evolved into a full **multi-threaded malware simulation framework** that mimics real-world payloads for red teaming and cybersecurity labs.

The executable is **hidden in a ZIP file** as a `.exe` disguised as a "Resume Viewer". Once opened by the victim, the payload silently activates, collects data, and sends it to a **local exfiltration server**.

---

## 🚀 Features

- ✅ **Keystroke Logger** using `pynput`
- ✅ **Webcam + Screen Capture** using `OpenCV`
- ✅ **Audio Recording** (via `sounddevice` & `pydub`)
- ✅ **Remote Kill Switch** (via GitHub `kill.txt`)
- ✅ **Auto Upload to HTTP Server** (Python-based)
- ✅ **Multi-threaded Execution** for parallel capture
- ✅ **Stealth Execution** (packaged `.exe` via `Auto-py-to-exe`)
- ✅ **Zipped Payload** to avoid suspicion
- 🔜 **Future Plan**: Host listener server publicly and implement AV bypassing techniques

---

## 📁 Folder Structure

```

malware-simulation/
├── key.py                # Core logger logic
├── screen\_capture.py     # Captures screenshots
├── cam\_capture.py        # Captures webcam footage
├── audio\_recorder.py     # Records ambient audio
├── upload.py             # Uploads logs to listener
├── kill\_switch.py        # Checks remote kill.txt
├── listener\_server.py    # HTTP Server for receiving logs
├── build.exe             # Packed payload via Auto-py-to-exe
├── resume\_viewer.zip     # ZIP with embedded .exe
├── logs/                 # Collected logs locally
└── README.md

````

---

## 🔧 How It Works

1. **User opens `resume.exe` (inside a zip)**.
2. The script launches in background and begins:
   - Logging keystrokes
   - Taking screenshots/webcam captures
   - Recording short audio clips
   - Uploading all data every 10–20 seconds
3. Periodically checks a **GitHub kill switch** to terminate execution safely.

---

## 🛠️ Tools & Libraries Used

- Python 3.x
- `pynput`
- `sounddevice`, `pydub`
- `opencv-python`
- `requests`
- `threading`, `os`, `time`, `subprocess`
- `ffmpeg` (silent integration)
- Auto-py-to-exe (to generate `.exe`)
- GitHub (for kill switch)

---

## 📦 How to Build

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
````

2. Build `.exe`:

   ```bash
   auto-py-to-exe
   # Select key.py as script, Onefile, Window-based, add hidden imports if needed
   ```

3. Embed `.exe` into a ZIP archive to deliver:

   ```bash
   zip resume_viewer.zip build.exe
   ```

---

## 🌐 Remote Kill Switch Setup

1. Create a **GitHub repository** with a file named `kill.txt`.
2. Add "1" (or any keyword) to trigger kill.
3. The script reads it and self-destructs if matched.

---

## 🤝 Contributing

Looking for collaborators to:

* Host listener on a public server
* Enhance AV evasion techniques
* Implement obfuscation and encryption for logs
* Design cleaner GUI wrapper for packaging
* To bypass antivirus and send it to victim via url

---

## 📚 Educational Purpose

This project aims to:

* Demonstrate real-world malware behaviors in a safe lab
* Educate ethical hackers, red teamers, and analysts
* Build hands-on knowledge of attack simulation and defenses

---

## ⚠️ Legal Note

Using this project against devices or individuals without **explicit permission** is strictly illegal and unethical. Always test in **virtual environments** or isolated labs.

---

## 📩 Contact

Let’s collaborate on red team tools, malware simulations, or infosec labs:

**LinkedIn:** \https://www.linkedin.com/in/sumit-raj-b75780291/

**GitHub:** \minizyperx

Here’s a `requirements.txt` file based on the typical libraries used in your malware simulation/keylogger project:

---

### ✅ `requirements.txt`

```
pynput==1.7.6
sounddevice==0.4.6
pydub==0.25.1
opencv-python==4.9.0.80
numpy==1.26.4
requests==2.31.0
```

### 🔧 Notes:

* `numpy` is required by OpenCV and `sounddevice`.
* `pydub` depends on `ffmpeg`, which must be installed separately on the system.
* You may also use a virtual environment:

  ```bash
  python -m venv venv
  source venv/bin/activate  # or venv\Scripts\activate on Windows
  pip install -r requirements.txt
  ```
