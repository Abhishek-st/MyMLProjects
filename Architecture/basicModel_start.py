# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QB5svW9YZ-lv1j995vkoS8Vdu1_ePDKi
"""

import torch 
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader

import torchvision.datasets as datasets
import torchvision.transforms as transforms

class NN(nn.odule):
  def __init__(self, input_size, num_classes):
    super(NN,self).__init__()
    self.fc1 = nn.Linear(input_size,50)
    self.fc2 = nn.Linear(50,num_classes)

  def forward(self,x):
    x = F.relu(self.fc1(x))
    x = self.fc2(x)

    return x

mod = NN(784,10)
x = torch.randn(64,784)

print(mod(x).shape)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

input_size = 784
num_classes = 10
lr = 0.001
batch_size = 64
num_epoch = 5

train_dataset = datasets.MNIST('',train=True, transform=transforms.ToTensor(), download = True)
train_loader = DataLoader(dataset = train_dataset, batch_size=batch_size, shuffle=True)

test_dataset = datasets.MNIST('/content',train=False, transform=transforms.ToTensor(), download = True)
test_loader = DataLoader(dataset = test_dataset, batch_size=batch_size, shuffle=True)

model = NN(input_size, num_classes).to(device)
# loss and optim

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=lr)

for epoch in range(num_epoch):
  # model.train()

  for idx,(data,targets) in enumerate(train_loader):
    data = data.to(device)
    targets = targets.to(device)

    data = data.reshape(data.shape[0],-1)

    scores = model(data)

    loss = criterion(scores,targets)

    optimizer.zero_grad()
    loss.backward()

    optimizer.step()

def check(loader,model):
  model.eval()
  num_correct = 0
  num_samples = 0

  with torch.no_grad():
    for x,y in  loader:
      x = x.to(device)
      y = y.to(device)

      x = x.reshape(x.shape[0], -1)
      scores = model(x)

      _ , predictions = scores.max(1)
      num_correct += (predictions == y).sum()
      num_samples += predictions.size(0)

  print(float(num_correct) / float(num_samples))


check(train_loader, model)
check(test_loader, model)
