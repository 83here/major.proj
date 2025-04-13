from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import threading
import torch

from lstm_model import LSTMForecaster
from live_data import simulate_data, buffer

# ✅ Lifespan handler to start simulate_data in the background
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Lifespan starting: simulate_data will run in background")
    threading.Thread(target=simulate_data, daemon=True).start()
    yield
    print("Lifespan shutting down")

# Create app with lifespan handler
app = FastAPI(lifespan=lifespan)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in prod!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
model = LSTMForecaster(input_size=3)
model.load("/model_data/lstm_forecaster.pth")

@app.get("/predict")
def get_prediction():
    if len(buffer) < 10:
        return {
            "message": "Insufficient data for prediction",
            "current_data": [x.tolist() for x in buffer],
            "prediction": None
        }

    input_seq = torch.cat(list(buffer), dim=0)
    prediction = model.predict(input_seq)

    return {
        "message": "Prediction successful",
        "current_data": [x.tolist() for x in buffer],
        "prediction": prediction.tolist()
    }
