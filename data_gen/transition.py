import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Simulation Parameters ---
rows = 1000
time = np.arange(0, rows)
noise_level = 0.03
cycle_duration = 4
omega = 2 * np.pi / cycle_duration  # 1 cycle every 5 seconds

# --- Generate X-axis: abrupt change from healthy to faulty at t=10s ---
x = []
for t in time:
    if t < 10:
        val = np.sin(omega * t) 
    else:
        val = np.sin(3 * omega * t) + np.sin(7 * omega * t)
    x.append(val)

# Optional Y/Z: just offset X
y = [val + 0.2 for val in x]
z = [val - 0.2 for val in x]

# --- Save to CSV ---
df = pd.DataFrame({
    "Time (s)": time,
    "X-axis (g)": x,
    "Y-axis (g)": y,
    "Z-axis (g)": z
})

# Update the path to your desired location
df.to_csv("transition.csv", index=False)
print("✅ transition.csv saved!")

# --- Visualization: View showing both healthy and faulty regions ---
plt.figure(figsize=(12, 4))
plt.plot(time, x, label='X-axis (g)', color='teal')
plt.axvline(10, color='red', linestyle='--', label='Fault Transition @ t=10s')

plt.title("Vibration Signal: Healthy to Faulty Transition")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (g)")
plt.xlim(5, 15)  # Show both sides of the transition
plt.ylim(-2.2, 2.2)
plt.xticks(np.arange(5, 16, 1))  # ticks every 1 second
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# --- Additional visualization showing more detail of the transition ---
plt.figure(figsize=(15, 8))

# Create a subplot grid
plt.subplot(2, 1, 1)
plt.plot(time, x, label='X-axis (g)', color='teal')
plt.axvline(10, color='red', linestyle='--', label='Fault Transition @ t=10s')
plt.title("Full Vibration Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (g)")
plt.xlim(0, 20)  # Show a wider view
plt.grid(True)
plt.legend()

# Zoomed view of the transition
plt.subplot(2, 1, 2)
plt.plot(time, x, label='X-axis (g)', color='teal')
plt.axvline(10, color='red', linestyle='--', label='Fault Transition @ t=10s')
plt.title("Zoomed Transition Region")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (g)")
plt.xlim(8, 12)  # Focused on the transition
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()