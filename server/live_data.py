import pandas as pd
import torch
from collections import deque
import time

# Global buffer shared with API
buffer = deque(maxlen=10)

# Path to your CSV file
CSV_PATH = "/Users/prasanna/Desktop/major.proj/data_gen/transition.csv"

def simulate_data():
    # Load the CSV file
    df = pd.read_csv(CSV_PATH)

    # Extract the x, y, z columns
    values = df[['X-axis (g)', 'Y-axis (g)', 'Z-axis (g)']].values  # shape: [T, 3]

    for row in values:
        # Convert to tensor of shape [1, 3] and append
        buffer.append(torch.tensor([row], dtype=torch.float32))
        time.sleep(1)  # Simulate 1 Hz data stream

    print("✅ Finished reading CSV file.")
