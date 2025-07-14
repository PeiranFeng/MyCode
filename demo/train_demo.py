import torch
import numpy as np
from torch import nn

x = torch.tensor([[1, 2, 3], [4, 5, 6]], dtype=torch.float32, requires_grad=False)
output = torch.tensor([[1, 2, 3], [4, 5, 6]], dtype=torch.float32, requires_grad=False)

W1 = nn.Parameter(torch.randn(3,3), requires_grad=True)
W2 = nn.Parameter(torch.randn(3,3), requires_grad=True)
W0 = nn.Parameter(torch.tensor([1], dtype=torch.float32), requires_grad=False)
# optimizer = torch.optim.SGD([W1, W2], lr=0.01, momentum=0.9)
optimizer = torch.optim.Adam([W1, W2], lr=0.1)
g = x @ W1
y = g @ W2
y = y + W0
with torch.no_grad():
    W0.data += 0.01 * torch.randn_like(W0)

loss = nn.MSELoss()(y, output)
loss.backward()
print('grad W2: ', W2.grad)

print('y: ', y)
print('W1: ', W1)
print('W2: ', W2)
print('W0: ', W0)
print('loss: ', loss.item())

for epoch in range(10):
    optimizer.zero_grad()
    g = x @ W1
    y = g @ W2
    loss = nn.MSELoss()(y, output)
    loss.backward()
    optimizer.step()
    print(f'Epoch {epoch+1}, Loss: {loss.item()}')

print('Final W1: ', W1)
print('Final W2: ', W2)
print('Final W0: ', W0)
print('Final y: ', y)
print('Final loss: ', loss.item())

if loss.item() < 1:
    torch.save({
        'W1': W1,
        'W2': W2,
        'W0': W0,
        'loss': loss.item()
    }, 'tensor_test.pth')
    print('Model saved successfully.')

