from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import threading
import torch

from lstm_model import LSTMForecaster
from live_data import simulate_data, buffer

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
model.load("/Users/prasanna/Desktop/major.proj/server/model_data/lstm_forecaster.pth")


from torch.nn import MSELoss

@app.get("/predict")
def get_prediction():
    buffer_list = list(buffer)
    buffer_len = len(buffer)

    # Case 1: Less than 10 – not enough data to predict
    if buffer_len < 10:
        return {
            "message": "Insufficient data for prediction",
            "current_data": [x.tolist() for x in buffer_list],
            "prediction": None,
            "true_future": None,
            "mse": None
        }

    # Prepare input
    input_seq = torch.cat(buffer_list[:10], dim=0)  # First 10
    
    # Case 2: 10 to 14 – predict, but no complete ground truth
    if 10 <= buffer_len < 15:
        prediction = model.predict(input_seq)
        true_future = buffer_list[10:]  # Partial ground truth
        return {
            "message": "Partial prediction and ground truth available",
            "current_data": [[x.tolist()] for x in buffer_list[:10]],
            "prediction": prediction.tolist(),
            "true_future": [x.tolist() for x in true_future],
            "mse": None
        }

    # Case 3: Exactly 15 – full prediction and ground truth
    if buffer_len == 15:
        prediction = model.predict(input_seq)
        true_future = torch.cat(buffer_list[10:], dim=0)
        mse_loss = MSELoss()(prediction, true_future).item()

        return {
            "message": "Full prediction with MSE",
            "current_data": [[x.tolist()] for x in buffer_list[:10]],
            "prediction": prediction.tolist(),
            "true_future": [x.tolist() for x in buffer_list[10:]],
            "mse": mse_loss
        }
