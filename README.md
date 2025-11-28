# 🧍‍♂️ Posture Safety App

A simple posture detection system that prevents you from sitting like a shrimp.  
It uses pose detection to track your body position and warns when you're slouching.

---

## 🚀 Features
- Real-time posture monitoring
- Frontend UI (camera + visualization)
- Backend API for posture logic
- Lightweight ML / pose detection
- Easy to run locally
- Can be extended for alerts, timers, logs, etc.

---

## 🧠 What Actually Happens
1. Webcam feeds are processed.
2. Pose landmarks (shoulder, neck, spine, etc.) are detected.
3. Posture metrics are calculated.
4. If posture drops below the threshold → user gets warned.

Not medical.  
Just trying to stop back pain.

---

## 📦 Project Structure
posture-safety-app/
│
├── backend/
│   ├── app.py              # Main FastAPI backend
│   ├── config.yaml         # Model + API configuration (classes, checkpoint path, etc.)
│   └── requirements.txt    # Python dependencies
│
└── frontend/
    ├── public/
    │   └── index.html      # App root HTML
    │
    ├── src/
    │   ├── App.js          # UI logic + API call
    │   ├── App.css         # Styling for UI components
    │   └── index.js        # React entry point
    │
    └── package.json        # Node dependencies + scripts


---

## 🛠️ Tech Stack
**Backend**
- Python
- Flask/FastAPI (depending on implementation)
- OpenCV / Mediapipe

**Frontend**
- React / JS
- Basic UI

---

## 🏃‍♂️ How to Run

### 🔹 Backend

---

## 📊 How Posture is Evaluated
- Neck + shoulder positions
- Spine angle
- Head tilt
- Relative ratios between joints

When the metrics cross a threshold → **bad posture**

---

## 💡 Ideas for Improvements
- Pose classification model
- Store history of posture
- Dashboard
- User profiles
- Alerts / notifications
- Mobile version

---

## 📌 Disclaimer
Not a medical device.
I am not your physiotherapist.
This app just screams at you when you sit like a goblin.

---
