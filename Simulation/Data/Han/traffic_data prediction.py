import torch
from torch import nn
from d2l import torch as d2l
import matplotlib.pyplot as plt

import numpy
import pandas as pd
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

import mpl_toolkits.axes_grid1.inset_locator


# 初始化网络权重的函数
def init_weights(m):
    if type(m) == nn.Linear:
        nn.init.xavier_uniform_(m.weight)


# 一个简单的多层感知机
def get_net():
    net = nn.Sequential(nn.Linear(4, 10),
                        nn.ReLU(),
                        nn.Linear(10, 1))
    net.apply(init_weights)
    return net


def train(net, train_iter, loss, epochs, lr):
    trainer = torch.optim.Adam(net.parameters(), lr)
    for epoch in range(epochs):
        for X, y in train_iter:
            trainer.zero_grad()
            l = loss(net(X), y)
            l.sum().backward()
            trainer.step()
        print(f'epoch {epoch + 1}, '
              f'loss: {d2l.evaluate_loss(net, train_iter, loss):f}')


if __name__ == '__main__':
    t = 644
    time = torch.arange(1, t + 1, dtype=torch.float32)
    cell_0_load = numpy.genfromtxt('saved_results\\Jun.27_15.51.30\\cell_0_total_load_results.csv',
                                   delimiter=',', names=True)
    cell_0 = cell_0_load['total_load']
    cell_load = torch.from_numpy(cell_0).float()
    d2l.plot(time, [cell_load], 'time', 'load', xlim=[1, 200], figsize=(6, 3))
    plt.show()

    tau = 4
    features = torch.zeros((t - tau, tau))
    for i in range(tau):
        features[:, i] = cell_load[i: t - tau + i]
    labels = cell_load[tau:].reshape((-1, 1))

    batch_size, n_train = 15, 644
    # 只有前n_train个样本用于训练
    train_iter = d2l.load_array((features[:n_train], labels[:n_train]), batch_size, is_train=True)

    # 平方损失。注意：MSELoss计算平方误差时不带系数1/2
    loss = nn.MSELoss(reduction='none')

    net = get_net()
    train(net, train_iter, loss, 15, 0.1)

    onestep_preds = net(features)
    d2l.plot([time, time[tau:]],
             [cell_load.detach().numpy(), onestep_preds.detach().numpy()], 'time',
             'x', legend=['data', '1-step preds'], xlim=[1, 200],
             figsize=(8, 4))
    plt.show()
