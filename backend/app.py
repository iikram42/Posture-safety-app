import io
import os
import yaml
from typing import Dict

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from PIL import Image

import torch
import torch.nn as nn
from torchvision import models, transforms


def load_config(config_path: str = "config.yaml") -> dict:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


cfg = load_config("config.yaml")

if cfg.get("device", "auto") == "cuda":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
elif cfg.get("device") == "cpu":
    device = torch.device("cpu")
else:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

IMG_SIZE = int(cfg.get("img_size", 224))
CLASS_NAMES = cfg.get("class_names", ["safe", "unsafe"])
NUM_CLASSES = int(cfg.get("num_classes", len(CLASS_NAMES)))
CHECKPOINT_PATH = cfg.get("model_checkpoint", "./best_model.pt")


def build_model(num_classes: int) -> nn.Module:
    model = models.resnet18(pretrained=False)
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes)
    return model


model = build_model(NUM_CLASSES)
if not os.path.exists(CHECKPOINT_PATH):
    raise FileNotFoundError(f"Model checkpoint not found at {CHECKPOINT_PATH}")

checkpoint = torch.load(CHECKPOINT_PATH, map_location=device)
state_dict = checkpoint.get("model_state_dict", checkpoint)
model.load_state_dict(state_dict)
model.to(device)
model.eval()


transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.CenterCrop(IMG_SIZE),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
    ),
])


app = FastAPI(
    title="Posture Safety API",
    description="Deep Learning-based SAFE / UNSAFE posture classifier.",
    version="1.0.0",
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictionResponse(BaseModel):
    predicted_class: str
    probabilities: Dict[str, float]
    unsafe_score: float
    device: str


def preprocess_image(file_bytes: bytes) -> torch.Tensor:
    try:
        image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {e}")
    tensor = transform(image).unsqueeze(0)
    return tensor


def predict_posture(image_bytes: bytes) -> PredictionResponse:
    tensor = preprocess_image(image_bytes).to(device)

    with torch.no_grad():
        outputs = model(tensor)
        probs = torch.softmax(outputs, dim=1)[0].cpu().numpy()

    pred_idx = int(probs.argmax())
    predicted_class = CLASS_NAMES[pred_idx] if pred_idx < len(CLASS_NAMES) else str(pred_idx)

    prob_dict = {CLASS_NAMES[i]: float(p) for i, p in enumerate(probs)}

    unsafe_idx = CLASS_NAMES.index("unsafe") if "unsafe" in CLASS_NAMES else 1
    unsafe_score = float(probs[unsafe_idx])

    return PredictionResponse(
        predicted_class=predicted_class,
        probabilities=prob_dict,
        unsafe_score=unsafe_score,
        device=str(device),
    )


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "device": str(device),
        "num_classes": NUM_CLASSES,
        "class_names": CLASS_NAMES,
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    if file.content_type is None or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Empty file.")

    try:
        prediction = predict_posture(file_bytes)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {e}")

    return prediction


@app.get("/")
def root():
    return {
        "message": "Posture Safety API. Use /predict with an image file.",
        "health_endpoint": "/health",
        "predict_endpoint": "/predict",
    }
