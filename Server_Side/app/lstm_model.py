import torch
import torch.nn as nn
import torch.optim as optim

class LSTMForecastModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers=1):
        super(LSTMForecastModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, input_size * 5)

    def forward(self, x):
        out, _ = self.lstm(x)          # x: [batch, 10, input_size]
        out = out[:, -1, :]            # [batch, hidden_size]
        out = self.fc(out)             # [batch, input_size * 5]
        return out.view(-1, 5, x.shape[2])  # [batch, 5, input_size]


class LSTMForecaster:
    def __init__(self, input_size=1, hidden_size=64, lr=0.001, device=None):
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = LSTMForecastModel(input_size, hidden_size).to(self.device)
        self.criterion = nn.MSELoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)

    def _create_sequences(self, data, window_size=10, target_size=5):
        X, Y = [], []
        for i in range(len(data) - window_size - target_size + 1):
            X.append(data[i:i+window_size])
            Y.append(data[i+window_size:i+window_size+target_size])
        return torch.stack(X), torch.stack(Y)

    def train(self, data, epochs=100, window_size=10, target_size=5):
        self.model.train()
        X, Y = self._create_sequences(data, window_size, target_size)
        X, Y = X.to(self.device), Y.to(self.device)

        for epoch in range(epochs):
            self.optimizer.zero_grad()
            output = self.model(X)
            loss = self.criterion(output, Y)
            loss.backward()
            self.optimizer.step()

            if epoch % 10 == 0:
                print(f"[Epoch {epoch}] Loss: {loss.item():.4f}")

    def predict(self, input_seq):
        """
        input_seq: torch tensor of shape [10, input_size]
        returns: torch tensor of shape [5, input_size]
        """
        self.model.eval()
        input_seq = input_seq.unsqueeze(0).to(self.device)  # [1, 10, input_size]
        with torch.no_grad():
            pred = self.model(input_seq)
        return pred.squeeze(0).cpu()  # [5, input_size]

    def rolling_forecast(self, data, start=10):
        """
        data: [T, input_size] - full time series
        returns: [N, 5, input_size] - rolling 5-step predictions
        """
        preds = []
        for t in range(start, len(data) - 5):
            input_seq = data[t-10:t]
            pred = self.predict(input_seq)
            preds.append(pred)
        return torch.stack(preds)

    def save(self, path):
        torch.save(self.model.state_dict(), path)

    def load(self, path):
        self.model.load_state_dict(torch.load(path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()
