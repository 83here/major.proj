import pandas as pd
import torch
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sklearn.metrics import mean_squared_error
from lstm_model import LSTMForecaster

# --- Load test data ---
csv_path = "data_gen/transition.csv"
df = pd.read_csv(csv_path)
data = df[["X-axis (g)", "Y-axis (g)", "Z-axis (g)"]].values
data = torch.tensor(data, dtype=torch.float32)  # shape: [T, 3]

# --- Load model ---
model = LSTMForecaster(input_size=3)
model.load("model_data/lstm_forecaster.pth")

# --- Init plot ---
fig, axs = plt.subplots(4, 1, figsize=(10, 8))
lines = {
    "input": [ax.plot([], [], label="Input")[0] for ax in axs[:3]],
    "pred": [ax.plot([], [], label="Forecast")[0] for ax in axs[:3]],
    "true": [ax.plot([], [], label="True")[0] for ax in axs[:3]],
    "mse": axs[3].plot([], [], label="5-step MSE", color="red")[0]
}
mse_vals = []

for ax, name in zip(axs[:3], ["X-axis", "Y-axis", "Z-axis"]):
    ax.set_xlim(0, 15)
    ax.set_ylim(torch.min(data)-0.2, torch.max(data)+0.2)
    ax.set_title(name)
    ax.legend()
    ax.grid(True)

axs[3].set_xlim(0, 100)
axs[3].set_ylim(0, 1)
axs[3].set_title("5-step MSE over time")
axs[3].legend()
axs[3].grid(True)

# --- Update function ---
def update(frame):
    t = frame + 10
    if t + 5 >= len(data):
        return []

    input_seq = data[t-10:t]         # [10, 3]
    true_future = data[t:t+5]        # [5, 3]
    pred_future = model.predict(input_seq)  # [5, 3]

    for i in range(3):
        lines["input"][i].set_data(range(10), input_seq[:, i].numpy())
        lines["pred"][i].set_data(range(10, 15), pred_future[:, i].numpy())
        lines["true"][i].set_data(range(10, 15), true_future[:, i].numpy())

    mse = mean_squared_error(true_future.numpy().flatten(), pred_future.numpy().flatten())
    mse_vals.append(mse)
    lines["mse"].set_data(range(len(mse_vals)), mse_vals)

    axs[3].set_xlim(0, max(100, len(mse_vals)))

    return lines["input"] + lines["pred"] + lines["true"] + [lines["mse"]]

# --- Animate ---
ani = animation.FuncAnimation(
    fig, update, frames=range(0, len(data) - 15),
    interval=500, blit=True, repeat=False
)

plt.tight_layout()
plt.show()
