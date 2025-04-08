
import pandas as pd
import torch
from sklearn.preprocessing import StandardScaler
from lstm_model import LSTMForecaster  # Updated import

def load_and_prepare_data(csv_path):
    # Step 1: Load CSV and select x, y, z
    df = pd.read_csv(csv_path)
    features = df[['X-axis (g)', 'Y-axis (g)', 'Z-axis (g)']].values  # shape: [T, 3]

    # Step 2: Normalize using StandardScaler
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    # Step 3: Convert to torch tensor
    data_tensor = torch.tensor(features_scaled, dtype=torch.float32)
    return data_tensor, scaler

if __name__ == "__main__":
    # Path to your CSV
    csv_path = "/Users/prasanna/Desktop/major.proj/data_gen/faulty.csv"

    # Load and preprocess
    data, scaler = load_and_prepare_data(csv_path)

    # Initialize and train model
    model = LSTMForecaster(input_size=3, hidden_size=64, lr=0.001)
    model.train(data, epochs=100, window_size=10, target_size=5)

    # Save model
    model.save("lstm_forecaster.pth")
    print("✅ Model trained and saved as 'lstm_forecaster.pth'")
