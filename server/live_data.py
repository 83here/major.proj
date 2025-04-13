# live_data.py
import pandas as pd
import torch
from collections import deque
import time

buffer = deque(maxlen=10)
CSV_PATH = "data_gen/transition.csv"

def simulate_data():
    print(" simulate_data() started!")

    try:
        df = pd.read_csv(CSV_PATH)
        print(f" Loaded CSV with {len(df)} rows")

        values = df[['X-axis (g)', 'Y-axis (g)', 'Z-axis (g)']].values

        for i, row in enumerate(values):
            tensor = torch.tensor([row], dtype=torch.float32)
            buffer.append(tensor)
            print(f" Row {i} added to buffer")
            time.sleep(1)

        print(" Finished pushing all data.")

    except Exception as e:
        print("❌ simulate_data() error:", e)
