# 🧍‍♂️ Posture Safety App — Technical Documentation

## 1. Overview
Posture Safety App is a deep learning–based posture classification system that evaluates a single image and predicts whether the captured posture is SAFE or UNSAFE. It returns class probabilities, an unsafe score, and device information. The project consists of a FastAPI backend (PyTorch ResNet18) and a React frontend.

> ⚠️ This project is not a medical diagnostic tool. It is for ergonomic awareness only.

---

## 2. Architecture
```
User → Browser UI → POST /predict → FastAPI → PyTorch Model → JSON Output
```

**Layers**
| Component | Technology | Responsibility |
|---------|-----------|--------------|
| Frontend | React | File upload, preview, result UI |
| API | FastAPI | Endpoints + validation |
| Model | PyTorch | Classification (safe/unsafe) |
| Config | YAML | Device, checkpoint, class metadata |

---

## 3. Directory Layout
```
posture-safety-app/
│
├── backend/
│   ├── app.py              # FastAPI inference server
│   ├── config.yaml         # Model, classes, device
│   └── requirements.txt    # Dependencies
│
└── frontend/
    ├── public/
    │   └── index.html      # Root HTML
    ├── src/
    │   ├── App.js          # UI logic + fetch
    │   ├── App.css         # Styles
    │   └── index.js        # React entrypoint
    └── package.json        # Node dependencies
```

---

## 4. Backend Model (PyTorch + FastAPI)
- Model: **ResNet18**
- Pretrained disabled
- Classification head replaced:
```
Linear(in_features, num_classes)
```
- Image transforms:
  - Resize → CenterCrop → Tensor
  - Normalize with ImageNet means/std

### Checkpoint Behavior
- If `best_model.pt` exists → load weights
- If not → log warning and run with random weights
  - API continues functioning

---

## 5. Endpoints

### `GET /health`
Returns model metadata.
Example:
```json
{
  "status": "ok",
  "device": "cpu",
  "num_classes": 2,
  "class_names": ["safe","unsafe"]
}
```

### `POST /predict`
Accepts multipart image upload.
Returns:
```json
{
  "predicted_class": "unsafe",
  "probabilities": {
    "safe": 0.33,
    "unsafe": 0.67
  },
  "unsafe_score": 0.67,
  "device": "cpu"
}
```

### `GET /`
Landing endpoint for Humans/Machines.

---

## 6. config.yaml
Example:
```yaml
device: auto
img_size: 224
class_names: ["safe", "unsafe"]
num_classes: 2
model_checkpoint: "./best_model.pt"
```
Adjusting this file does not require changing code.

---

## 7. Frontend Logic (React)
- Upload via `<input type="file">`
- Local preview via `URL.createObjectURL`
- POST form data → `/predict`
- Shows:
  - severity badge (safe/unsafe)
  - predicted class
  - unsafe %
  - device
  - probability list

Graceful error handling for:
- backend offline
- invalid MIME
- empty file

---

## 8. Probability Interpretation
`unsafe_score` = model probability for the class `"unsafe"`.

Recommended ranges:
- **0.0–0.4** → likely safe
- **0.4–0.6** → uncertain/borderline
- **0.6+** → unsafe posture

---

## 9. Suggested Training Workflow
(Not included in repo)

**Dataset**
- Sitting images labeled safe/unsafe
- Variation of clothing, angles, lighting

**Training setup**
- Base model: ResNet18
- Loss: CrossEntropy
- Optimizer: Adam (LR=1e−4)
- Epochs: 20–40
- Augmentations (recommended):
  - random crop
  - flip
  - color jitter

**Export checkpoint**
```python
torch.save({"model_state_dict": model.state_dict()}, "best_model.pt")
```

---

## 10. Known Limitations
- Single frame analysis
- No pose keypoints
- No motion or time context
- Lighting sensitive
- Dataset bias influences results

---

## 11. Roadmap / Improvements
| Category | Idea |
|--------|------|
| CV | Integrate MediaPipe body landmarks |
| ML | Vision Transformers |
| UX | Webcam live mode |
| DevOps | Docker deployment |
| Ergonomics | Posture logs over time |
| Safety | Reject blurry/low-resolution input |

---

## 12. How to Run

### Backend
```
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```

### Frontend
```
cd frontend
npm install
npm start
```

Open:
```
http://localhost:3000
```

---

## 13. Disclaimer
This application is not a medical device.  
It does not diagnose injuries or posture disorders.  
It is intended for research, demonstration, and ergonomic awareness only.

---

## 14. License
Educational and non-commercial recommended usage.
