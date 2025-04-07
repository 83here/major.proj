from fastapi import FastAPI
from app.lstm_model import LSTMForecaster
from app.live_data import buffer
import torch

app = FastAPI()

# Initialize and load the model
model = LSTMForecaster()
model.load("models/lstm_model.pth")  # Make sure the model is saved here

@app.get("/predict")
def get_prediction():
    current_data = [x.item() for x in buffer]

    # Not enough data to predict yet, just return current buffer
    if len(buffer) < 10:
        return {
            "message": "Insufficient data for prediction",
            "current_data": current_data,
            "prediction": None
        }

    # Enough data — make prediction
    input_seq = torch.stack(list(buffer))  # Shape: [10, 1]
    prediction = model.predict(input_seq)  # Shape: [5, 1]

    return {
        "message": "Prediction successful",
        "current_data": current_data,
        "prediction": prediction.squeeze(-1).tolist()  # [5]
    }
