import torch
from torch import nn
from d2l import torch as d2l
import matplotlib.pyplot as plt
import csv_record
import time, os
import datetime

import numpy
import pandas as pd
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

import mpl_toolkits.axes_grid1.inset_locator


def get_net():
    net = nn.Sequential(nn.Linear(in_features, 2))
    return net


def log_rmse(net, features, labels):
    # 为了在取对数时进一步稳定该值，将小于1的值设置为1
    clipped_preds = torch.clamp(net(features), 1, float('inf'))
    # rmse = torch.sqrt(loss(torch.log(clipped_preds),
    #                       torch.log(labels)))
    rmse = torch.sqrt(loss(net(features), labels))
    return rmse.item()


def train(net, train_features, train_labels, test_features, test_labels,
          num_epochs, learning_rate, weight_decay, batch_size, record_saved):
    train_ls, test_ls = [], []
    # print(train_features.shape, train_labels.shape)
    train_iter = d2l.load_array((train_features, train_labels), batch_size)

    optimizer = torch.optim.Adam(net.parameters(),
                                 lr=learning_rate,
                                 weight_decay=weight_decay)
    for epoch in range(num_epochs):
        for X, y in train_iter:
            optimizer.zero_grad()
            l = loss(net(X), y)
            l.backward()
            optimizer.step()
        preds = net(train_features)
        # print(preds)
        ls_rmse = torch.sqrt(loss(preds, train_labels)).item()
        train_ls.append(ls_rmse)
        if test_labels is not None:
            test_preds = net(test_features)
            test_ls_rmse = torch.sqrt(loss(test_preds, test_labels)).item()
            test_ls.append(test_ls_rmse)

        if record_saved:
            pred_acc(test_preds, test_labels, epoch)
            csv_record.train_test_ls.append(
                [epoch, ls_rmse, test_ls_rmse])

    csv_record.save_result_csv(folder_path)

    return train_ls, test_ls


def pred_acc(preds, labels, epoch):
    preds = preds.detach().numpy()
    preds_ts = preds[:, 0]
    for i in range(len(preds_ts)):
        if preds_ts[i] >= 1.5:
            preds_ts[i] = 2.0
        elif 1 <= preds_ts[i] < 1.5:
            preds_ts[i] = 1.0
        elif 0 <= preds_ts[i] < 1:
            preds_ts[i] = 0.0

    pred_cb = preds[:, 1]
    for i in range(len(pred_cb)):
        if pred_cb[i] >= 0.5:
            pred_cb[i] = 1.0
        elif pred_cb[i] < 0.5:
            pred_cb[i] = 0.0
    before_clipped = preds
    preds[:, 0] = preds_ts
    preds[:, 1] = pred_cb
    csv_record.preds_labels.append([epoch, before_clipped, preds])
    preds[:, 0] = preds_ts
    preds[:, 1] = pred_cb

    ts_acc = 0
    cb_acc = 0
    for i in range(len(labels[:, 0])):
        if preds[i, 0] == labels[i, 0]:
            ts_acc = ts_acc + 1
        if preds[i, 1] == labels[i, 1]:
            cb_acc = cb_acc + 1

    ts_acc_per = ts_acc / len(labels[:, 0])
    cb_acc_per = cb_acc / len(labels[:, 0])

    csv_record.labels_acc.append([epoch, ts_acc_per, cb_acc_per])

    return


def get_k_fold_data(k, i, X, y):
    assert k > 1
    fold_size = X.shape[0] // k
    X_train, y_train = None, None
    for j in range(k):
        idx = slice(j * fold_size, (j + 1) * fold_size)
        X_part, y_part = X[idx, :], y[idx]
        if j == i:
            X_valid, y_valid = X_part, y_part
        elif X_train is None:
            X_train, y_train = X_part, y_part
        else:
            X_train = torch.cat([X_train, X_part], 0)
            y_train = torch.cat([y_train, y_part], 0)
    return X_train, y_train, X_valid, y_valid


def k_fold(k, X_train, y_train, num_epochs, learning_rate, weight_decay,
           batch_size):
    train_l_sum, valid_l_sum = 0, 0
    for i in range(k):
        data = get_k_fold_data(k, i, X_train, y_train)
        net = get_net()
        train_ls, valid_ls = train(net, *data, num_epochs, learning_rate,
                                   weight_decay, batch_size, record_saved=False)
        # print('train_ls', train_ls)
        train_l_sum += train_ls[-1]
        # print(valid_ls)
        valid_l_sum += valid_ls[-1]

        if i == 0:
            d2l.plot(list(range(1, num_epochs + 1)), [train_ls, valid_ls],
                     xlabel='epoch', ylabel='rmse', xlim=[1, num_epochs],
                     legend=['train', 'valid'], yscale='log')
            plt.savefig(f'saved_results/{current_time}/train_valid_k0_ls.pdf')
            plt.show()
        elif i == 1:
            d2l.plot(list(range(1, num_epochs + 1)), [train_ls, valid_ls],
                     xlabel='epoch', ylabel='rmse', xlim=[1, num_epochs],
                     legend=['train', 'valid'], yscale='log')
            plt.savefig(f'saved_results/{current_time}/train_valid_k1_ls.pdf')
            plt.show()
        elif i == 2:
            d2l.plot(list(range(1, num_epochs + 1)), [train_ls, valid_ls],
                     xlabel='epoch', ylabel='rmse', xlim=[1, num_epochs],
                     legend=['train', 'valid'], yscale='log')
            plt.savefig(f'saved_results/{current_time}/train_valid_k2_ls.pdf')
            plt.show()
        elif i == 3:
            d2l.plot(list(range(1, num_epochs + 1)), [train_ls, valid_ls],
                     xlabel='epoch', ylabel='rmse', xlim=[1, num_epochs],
                     legend=['train', 'valid'], yscale='log')
            plt.savefig(f'saved_results/{current_time}/train_valid_k3_ls.pdf')
            plt.show()
        elif i == 4:
            d2l.plot(list(range(1, num_epochs + 1)), [train_ls, valid_ls],
                     xlabel='epoch', ylabel='rmse', xlim=[1, num_epochs],
                     legend=['train', 'valid'], yscale='log')
            plt.savefig(f'saved_results/{current_time}/train_valid_k4_ls.pdf')
            plt.show()
        # print(f'折{i + 1}，训练log rmse{float(train_ls[-1]):f}, '
        #      f'验证log rmse{float(valid_ls[-1]):f}')
    return train_l_sum / k, valid_l_sum / k


def train_and_pred(train_features, test_features, train_labels, test_labels,
                   num_epochs, lr, weight_decay, batch_size):
    net = get_net()
    train_ls, test_ls = train(net, train_features, train_labels, test_features, test_labels,
                              num_epochs, lr, weight_decay, batch_size, record_saved=True)
    d2l.plot(numpy.arange(1, num_epochs + 1), [train_ls, test_ls], xlabel='epoch',
             ylabel='log rmse', xlim=[1, num_epochs], legend=['train', 'test'], yscale='log')
    plt.savefig(f'saved_results/{current_time}/train_test_ls.pdf')
    plt.show()

    ts_accuracy = []
    cb_accuracy = []
    for i in range(len(csv_record.labels_acc)):
        ts_accuracy.append(csv_record.labels_acc[i][1])
        cb_accuracy.append(csv_record.labels_acc[i][2])
    d2l.plot(list(range(1, num_epochs + 1)), [ts_accuracy, cb_accuracy], xlabel='epoch',
             ylabel='rmse', xlim=[1, num_epochs],
             legend=['ts_acc', 'cb_acc'], yscale='log')
    plt.savefig(f'saved_results/{current_time}/ts_cb_acc.pdf')
    plt.show()
    # print(train_ls)
    # print(f'训练log rmse：{float(train_ls[-1]):f}')

    preds = net(test_features).detach().numpy()
    print(preds)

    return


if __name__ == '__main__':
    start_time = time.time()
    current_time = datetime.datetime.now().strftime('%b.%d_%H.%M.%S')
    folder_path = f'saved_results/{current_time}/modified_samples1200_400_1.1prb_60_bs32_lr0.01/cell_6'
    try:
        os.makedirs(folder_path)
    except FileExistsError:
        print("Folder already exists")

    data = pd.read_csv(
        "D:\\data generation for traffic steering test3\\saved_results\\Jul.04_15.31.26\\cell_6_total_load_results.csv")
    train_data = data[:1200]
    test_data = data[1200:1600]

    test_features = pd.concat((test_data.iloc[:, 1], test_data.iloc[:, 4]), axis=1)
    train_features = pd.concat((train_data.iloc[:, 1], train_data.iloc[:, 4]), axis=1)

    train_labels = pd.concat((train_data.iloc[:, 2], train_data.iloc[:, 3]), axis=1)
    test_labels = pd.concat((test_data.iloc[:, 2], test_data.iloc[:, 3]), axis=1)

    train_features = torch.tensor(train_features.values, dtype=torch.float32)
    test_features = torch.tensor(test_features.values, dtype=torch.float32)
    train_labels = torch.tensor(train_labels.values, dtype=torch.float32)
    test_labels = torch.tensor(test_labels.values, dtype=torch.float32)

    loss = nn.MSELoss()
    in_features = train_features.shape[1]

    k, num_epochs, lr, weight_decay, batch_size = 5, 1000, 0.01, 0, 32
    train_l, valid_l = k_fold(k, train_features, train_labels, num_epochs, lr,
                              weight_decay, batch_size)
    # print(f'{k}-折验证: 平均训练log rmse: {float(train_l):f}, '
    #      f'平均验证log rmse: {float(valid_l):f}')

    train_and_pred(train_features, test_features, train_labels, test_labels,
                   num_epochs, lr, weight_decay, batch_size)
