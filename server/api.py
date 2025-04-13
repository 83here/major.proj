from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 👈 Add this
from lstm_model import LSTMForecaster
from live_data import buffer
import torch

app = FastAPI()

# 👇 Add this block to allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 You can restrict this to your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    input_seq = torch.cat(list(buffer), dim=0)  # [10, 3]
    prediction = model.predict(input_seq)        # [5, 3]

    return {
        "message": "Prediction successful",
        "current_data": [x.tolist() for x in buffer],
        "prediction": prediction.tolist()
    }
