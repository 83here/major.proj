import numpy as np
import pandas as pd

# --- Settings for Healthy Signal ---
rows = 1000                  # 250 seconds = 50 cycles
cycle_duration = 4         # 1 cycle every 4 seconds
freq = 1 / cycle_duration   # Hz
omega = 2 * np.pi * freq    # Angular frequency
noise_level = 0.03          # Smaller noise for healthy signal

# --- Time Vector (1 reading per second) ---
time = np.arange(0, rows)

# --- Clean Sine Wave for Each Axis ---
x = np.sin(omega * time) + noise_level * np.random.randn(rows)
y = np.sin(omega * time + np.pi/4) + noise_level * np.random.randn(rows)
z = np.sin(omega * time + np.pi/2) + noise_level * np.random.randn(rows)

# --- Create DataFrame ---
df = pd.DataFrame({
    "Time (s)": time,
    "X-axis (g)": x,
    "Y-axis (g)": y,
    "Z-axis (g)": z
})

# --- Save to CSV ---
df.to_csv("/Users/prasanna/Desktop/major.proj/data_gen/healthy.csv", index=False)

print("✅ healthy.csv generated: 250 rows (clean signal, 1 cycle every 5 seconds).")
