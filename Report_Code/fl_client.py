import flwr as fl
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.datasets import make_regression
from torch.utils.data import DataLoader, TensorDataset
from blockchain_logger import SimpleLedger

# Dummy local model for each client
class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 1)
        )

    def forward(self, x):
        return self.net(x)

def get_data(seed=42):
    X, y = make_regression(n_samples=100, n_features=2, noise=0.2, random_state=seed)
    return DataLoader(TensorDataset(torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)), batch_size=16)

class FlowerClient(fl.client.NumPyClient):
    def __init__(self, model, trainloader):
        self.model = model
        self.trainloader = trainloader
        self.loss_fn = nn.MSELoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.01)

    def get_parameters(self, config): return [val.cpu().numpy() for val in self.model.state_dict().values()]

    def set_parameters(self, parameters):
        for param, new in zip(self.model.state_dict().keys(), parameters):
            self.model.state_dict()[param].copy_(torch.tensor(new))

    def fit(self, parameters, config):
        self.set_parameters(parameters)
        self.model.train()
        for epoch in range(3):
            for X_batch, y_batch in self.trainloader:
                y_pred = self.model(X_batch).squeeze()
                loss = self.loss_fn(y_pred, y_batch)
                loss.backward()
                self.optimizer.step()
                self.optimizer.zero_grad()

        # Evaluation on training data for demo purposes
        self.model.eval()
        X_all, y_all = next(iter(DataLoader(self.trainloader.dataset, batch_size=len(self.trainloader.dataset))))
        with torch.no_grad():
            preds = self.model(X_all).squeeze()
            acc = 1 - torch.mean((preds - y_all) ** 2).item()  # pseudo-accuracy using inverse MSE

        # Log contribution
        tokens = int(acc * 100)
        ledger.log_contribution(node_id="booth-123", accuracy=acc, tokens_awarded=tokens)

        return self.get_parameters(config), len(self.trainloader.dataset), {}


    def evaluate(self, parameters, config):
        self.set_parameters(parameters)
        return 0.0, len(self.trainloader.dataset), {}

if __name__ == "__main__":
    torch.manual_seed(0)
    ledger = SimpleLedger()
    client = FlowerClient(SimpleModel(), get_data(seed=123))
    fl.client.start_numpy_client(server_address="localhost:8080", client=client)
