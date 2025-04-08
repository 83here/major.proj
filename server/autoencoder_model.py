import torch
import torch.nn as nn

class TemporalAutoencoder(nn.Module):
    def __init__(self, input_dim=30, latent_dim=8):
        super(TemporalAutoencoder, self).__init__()
        
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 16),
            nn.ReLU(),
            nn.Linear(16, latent_dim)
        )
        
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 16),
            nn.ReLU(),
            nn.Linear(16, input_dim)
        )

    def forward(self, x):
        z = self.encoder(x)
        return self.decoder(z)

    def load(self, path):
        self.load_state_dict(torch.load(path, map_location=torch.device("cpu")))
        self.eval()

    def save(self, path):
        torch.save(self.state_dict(), path)
