import torch
import numpy as np
from torch import nn

class SimpleModel(nn.Module):
    def __init__(
            self, 
            input_dim: int, 
            hidden_dim: int, 
            num_layers: int
        ):
        super().__init__()
        self.layers = nn.ModuleList([
            nn.Linear(input_dim, hidden_dim)
            for _ in range(num_layers)
        ])
        self.final = nn.Linear(hidden_dim, 1)
    
    def forward(self, x):
        for layer in self.layers:
            y = layer(x)
            y = torch.relu(y)
            y = nn.Dropout(0.2)(y)
        return self.final(y)

def train_loop(
        model: torch.tensor, 
        optimizer: torch.optim.Optimizer,
        criterion: nn.Module,
        x_train: torch.tensor,
        y_train: torch.tensor,
        epochs: int=10
    ):
    for epoch in range(epochs):
        optimizer.zero_grad()
        outputs = model(x_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()
        print(f'Epoch {epoch+1}, Loss: {loss.item()}')

def generate_data(num_samples: int=100, input_dim: int=4):
    X = torch.randn(num_samples, input_dim)
    weights = torch.tensor([1.0, -0.5, 0.3, 0.2], dtype=torch.float32)
    y = (X @ weights).unsqueeze(1) + torch.randn(num_samples, 1) * 0.1
    return X, y

if __name__ == '__main__':
    criterion = nn.MSELoss()
    input_dim = 4
    hidden_dim = 32
    num_layers = 2
    lr = 0.01
    model = SimpleModel(input_dim, hidden_dim, num_layers)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    x_train, y_train = generate_data(1000, input_dim)
    x_test, y_test = generate_data(200, input_dim)
    
    model.train()
    train_loop(model, optimizer, criterion, x_train, y_train, epochs=100)

    model.eval()
    with torch.no_grad():
        test_outputs = model(x_test)
        test_loss = criterion(test_outputs, y_test)
        print(f'Test Loss: {test_loss.item()}')