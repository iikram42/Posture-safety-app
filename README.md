# 🧍‍♂️ Posture Safety App

A simple posture detection system that prevents you from sitting like a shrimp. It uses pose detection to track your body position and warns you when you're slouching.

## 🚀 Features
- Real-time posture evaluation
- Frontend UI (image upload + visualization)
- Backend REST API for inference
- Lightweight ML / posture classification
- Easy to run locally
- Extendable (alerts, logs, dashboards, etc.)

## 🧠 How It Works
1. User uploads a posture image/frame.
2. The backend extracts pose features.
3. Model computes posture safety probability.
4. Result → "safe" or "unsafe".

> ⚠️ Not medical. Just trying to stop back pain.

## 📦 Project Structure
posture-safety-app/
│
├── backend/
│   ├── app.py              # FastAPI backend server
│   ├── config.yaml         # Model/device/settings configuration
│   └── requirements.txt    # Python dependencies
│
└── frontend/
    ├── public/
    │   └── index.html      # Root HTML
    ├── src/
    │   ├── App.js          # UI + API calls
    │   ├── App.css         # Styling
    │   └── index.js        # React entry point
    └── package.json        # JS dependencies + scripts

## 🛠️ Tech Stack
Backend:
- Python
- FastAPI + Uvicorn
- Torch / Torchvision
- Pillow
- YAML config

Frontend:
- React
- Fetch API
- CSS UI

## 🏃‍♂️ How to Run Locally

### Backend
cd backend
pip install -r requirements.txt
uvicorn app:app --reload

Backend URL:
http://127.0.0.1:8000

Swagger API Docs:
http://127.0.0.1:8000/docs

### Frontend
cd frontend
npm install
npm start

Frontend URL:
http://localhost:3000

## 📊 How Posture is Evaluated
- Shoulder alignment
- Neck tilt
- Spine angle
- Relative ratios between pose joints
When thresholds are crossed → posture flagged as unsafe.

## 💡 Future Improvements
- Train an actual pose classifier
- Posture history storage
- Analytics dashboard
- User profiles
- Alerts / reminders
- Mobile app version

## 📌 Disclaimer
Not a medical device.
I am not your physiotherapist.
This app just screams at you when you sit like a goblin.
