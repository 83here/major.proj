import numpy as np
import pandas as pd

# --- Simulation Parameters ---
rows = 1000               # 1000 seconds = 1000 samples (1 sample/sec)
noise_level = 0.05
cycle_duration = 4       # One full sine cycle every 4 seconds
omega = 2 * np.pi / cycle_duration  # Angular frequency

# --- Time vector (1 reading per second) ---
time = np.arange(0, rows)

# --- Faulty Vibration Data: sin(3ωt) + sin(7ωt) + noise ---
x = np.sin(3 * omega * time) + np.sin(7 * omega * time) + noise_level * np.random.randn(rows)
y = np.sin(3 * omega * time + np.pi/4) + np.sin(7 * omega * time + np.pi/3) + noise_level * np.random.randn(rows)
z = np.sin(3 * omega * time + np.pi/2) + np.sin(7 * omega * time + np.pi/6) + noise_level * np.random.randn(rows)

# --- Create DataFrame ---
df = pd.DataFrame({
    "Time (s)": time,
    "X-axis (g)": x,
    "Y-axis (g)": y,
    "Z-axis (g)": z
})

# --- Save to CSV ---
df.to_csv("data_gen/faulty.csv", index=False)

print("faulty.csv generated with sin(3ωt) + sin(7ωt): 1000 rows, simulating sharp, faulty vibration with 5s cycle.")
