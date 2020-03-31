import torch
import torch.utils.data
import torch.backends.cudnn
import torch.cuda
import torch.optim as optim
import numpy as np
import random
import observers


class TrainConfig:
    def __init__(self, trainset, batch_size, epochs, lr, momentum, criterion, seed=None):
        __set_seed(seed)
        self.trainset_loader = torch.utils.data.DataLoader(
            trainset,
            batch_size=batch_size,
            shuffle=True
        )
        self.epochs = epochs
        self.lr = lr
        self.momentum = momentum
        self.criterion = criterion


def train_network(network, config, observer=observers.EmptyObserver()):
    optimizer = optim.SGD(network.parameters(), lr=config.lr, momentum=config.momentum)
    for epoch in range(config.epochs):
        for iteration, data in enumerate(config.trainset_loader, 0):
            inputs, labels = data
            optimizer.zero_grad()
            outputs = network(inputs)
            loss = config.criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            observer.update(network, epoch, iteration)


def __set_seed(seed):
    """
    Set seed for all torch func and methods.
    See ref: https://github.com/pytorch/pytorch/issues/7068
    """
    torch.manual_seed(seed)
    np.random.seed(seed)  # Numpy module.
    random.seed(seed)  # Python random module.
    torch.manual_seed(seed)
    torch.backends.cudnn.benchmark = seed is None
    torch.backends.cudnn.deterministic = seed is not None