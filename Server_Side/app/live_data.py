import pandas as pd
import torch
from collections import deque
import time

# Global buffer shared with API
buffer = deque(maxlen=10)

# Path to your CSV file
CSV_PATH = "data/sample_data.csv"  # Make sure to place the CSV in a /data folder

def simulate_data():
    # Load the CSV file
    df = pd.read_csv(CSV_PATH)

    # Assume column of interest is named "value"
    values = df["value"].values  # Adjust column name if needed

    for val in values:
        # Push value to buffer as a tensor
        buffer.append(torch.tensor([[val]], dtype=torch.float32))
        time.sleep(1)  # Simulate real-time by waiting 1 second

    print("Finished reading CSV file.")
