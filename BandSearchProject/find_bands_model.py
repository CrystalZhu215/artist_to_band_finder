import numpy as np
import matplotlib.pyplot as plt
import torch
from torch import nn

class NeuralNetwork(nn.Module):
    def __init__(self, input_dim, hidden_dim_1, hidden_dim_2, output_dim):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_Stack = nn.Sequential(
            nn.Linear(input_dim, hidden_dim_1),
            nn.ReLU(),
            nn.Linear(hidden_dim_1, hidden_dim_2),
            nn.ReLU(),
            nn.Linear(hidden_dim_2, output_dim)
        )
            
    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
print(f"Using {device} device")

model = NeuralNetwork(1000, 512, 512, 100).to(device)

x_train = np.load('x_train.npy')
y_train = np.load('y_train.npy')

optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
loss_fn = torch.nn.MSELoss()

losses = []

for t in range(0, 1000):
    optimizer.zero_grad()
    y_pred = model.forward(x_train)
    loss = loss_fn(y_pred, y_train)
    losses.append(loss)
    loss.backward()
    optimizer.step()

print('Inital loss:', losses[0])
print('Final loss:', losses[-1])

plt.plot(np.range(1000), losses)
plt.x_label('Time')
plt.y_label('Loss')
plt.show()