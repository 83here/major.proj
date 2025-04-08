from fastapi import FastAPI
from lstm_model import LSTMForecaster
from live_data import buffer
import torch

app = FastAPI()

# Initialize and load the model
model = LSTMForecaster(input_size=3)  # 3 axes: X, Y, Z
model.load("/Users/prasanna/Desktop/major.proj/server/model_data/lstm_forecaster.pth")

@app.get("/predict")
def get_prediction():
    if len(buffer) < 10:
        return {
            "message": "Insufficient data for prediction",
            "current_data": [x.tolist() for x in buffer],
            "prediction": None
        }

    # Stack tensors from buffer to shape [10, 3]
    input_seq = torch.cat(list(buffer), dim=0)  # each x is [1, 3], result is [10, 3]
    
    prediction = model.predict(input_seq)  # Shape: [5, 3]

    return {
        "message": "Prediction successful",
        "current_data": [x.tolist() for x in buffer],
        "prediction": prediction.tolist()  # Shape: [5, 3]
    }
