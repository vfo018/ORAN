from keras.layers import Dropout
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from config import *
from keras.models import load_model
import matplotlib.pyplot as plt



my_data = pd.read_table('output_handover_scenario_training_processed.csv', sep=',')
cell_load = my_data.iloc[0:12096, 7:8].values

#LSTM Nextwork
sc = MinMaxScaler(feature_range=(0, 1))
cell_load_scaled = sc.fit_transform(cell_load[:])
training_set_scaled = []
for i in range(0, len(cell_load_scaled), CELL_NUMBER):
    temp = []
    for j in range(0, CELL_NUMBER):
        temp.append(cell_load_scaled[i + j][0])
    training_set_scaled.append(temp)

training_set_scaled = np.array(training_set_scaled)
time_step = 10
X_train = []
y_train = []
for i in range(time_step, len(training_set_scaled)):
    X_train.append(training_set_scaled[i-time_step:i, :])
    y_train.append(training_set_scaled[i, :])
X_train, y_train = np.array(X_train), np.array(y_train)

# regressor = Sequential()
#
# # Adding the first LSTM layer and some Dropout regularisation
# regressor.add(LSTM(units = 128, return_sequences = True, input_shape = (X_train.shape[1], X_train.shape[2])))
# regressor.add(Dropout(0.1))
#
# # Adding a second LSTM layer and some Dropout regularisation
# regressor.add(LSTM(units = 128, return_sequences = True))
# regressor.add(Dropout(0.1))
#
# # Adding a third LSTM layer and some Dropout regularisation
# regressor.add(LSTM(units = 128, return_sequences = True))
# regressor.add(Dropout(0.1))
#
# # Adding a fourth LSTM layer and some Dropout regularisation
# regressor.add(LSTM(units = 128))
# regressor.add(Dropout(0.1))
#
# # Adding the output layer
# regressor.add(Dense(units = CELL_NUMBER))
#
# # Compiling the RNN
# regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')
#
# # Fitting the RNN to the Training set
# history = regressor.fit(X_train, y_train, epochs=2000, batch_size=100)
# losses = history.history['loss']
# np.save('lstm-cell-load-1-losses.npy', losses)
# regressor.save('lstm-cell-load-1.keras')


regressor = load_model('lstm-cell-load-1.keras')
test_data = pd.read_table('output_handover_scenario_testing_processed.csv', sep=',')
cell_load_test = test_data .iloc[0:4200, 7:8].values
cell_load_test = sc.transform(cell_load_test)
test_set_scaled = []
for i in range(0, len(cell_load_test), CELL_NUMBER):
    temp = []
    for j in range(0, CELL_NUMBER):
        temp.append(cell_load_test[i + j][0])
    test_set_scaled.append(temp)
X_test, real_cell_load = [], []
for i in range(time_step, len(test_set_scaled)):
    X_test.append(test_set_scaled[i-time_step:i])
    real_cell_load.append(test_set_scaled[i])
X_test = np.array(X_test)
real_cell_load = sc.inverse_transform(np.array(real_cell_load))
predicted_cell_load = sc.inverse_transform(regressor.predict(X_test)).astype(int)

plt.figure(figsize=(14, 8))
t = np.arange(10, 600)
for i in range(CELL_NUMBER):
    plt.plot(t, real_cell_load[:, i], label=f'Real Cell {i+1} Load')
    plt.plot(predicted_cell_load[:, i], linestyle='--', label=f'Predicted Cell {i+1} Load')

# matplotlib.use('Agg')
plt.title('Real vs Predicted Cell Load')
plt.xlabel('t')
plt.ylabel('Cell Load')
plt.legend()
plt.show()
# plt.savefig('cell_load_comparison.png')



# # plt.figure(1)
# # # real_label_plot_y = []
# # # real_label_plot_x = []
# # # for i, v in enumerate(real_label):
# # #     if v >= 1:
# # #         real_label_plot_y.append(v)
# # #         real_label_plot_x.append(i)
# # #         # plt.plot(v, color='red')
# # plt.plot(real_label, color = 'red', label = 'Real Label')
# # # plt.plot(label='Real Label')
# # # plt.title('Label Prediction')
# # plt.axis([0, len(real_label) + 1, -1.5, 1.5])
# # plt.title('Real Label')
# # plt.xlabel('Time')
# # plt.ylabel('Retransmission Signal')
# # plt.legend()
# # plt.show()
# #
# # plt.figure(2)
# # predicted_label_plot_y0 = []
# # predicted_label_plot_x0 = []
# # for i, v in enumerate(predicted_label):
# #     if v >= 0:
# #         predicted_label_plot_y0.append(1)
# #         predicted_label_plot_x0.append(i)
# #     else:
# #         predicted_label_plot_y0.append(-1)
# #         predicted_label_plot_x0.append(i)
# # plt.plot(predicted_label_plot_x0, predicted_label_plot_y0, color = 'blue', label = 'Corrected Label Predicted By RNN')
# # plt.axis([0, len(real_label) + 1, -1.5, 1.5])
# # plt.title('Label Prediction')
# # plt.xlabel('Time')
# # plt.ylabel('Retransmission Signal')
# # plt.legend()
# # plt.show()
# # n = 0
# # for i, v in enumerate(predicted_label_plot_y0):
# #     if v == real_label[i][0]:
# #         n += 1
# #
# #
# # fitting_rate = n/len(real_label)
# #
# # plt.figure(3)
# # predicted_label_plot_y = []
# # predicted_label_plot_x = []
# # for i, v in enumerate(predicted_label):
# #     # if v == -1 or v == 1:
# #     predicted_label_plot_y.append(v)
# #     predicted_label_plot_x.append(i)
# # plt.plot(predicted_label_plot_x, predicted_label_plot_y, color = 'blue', label = 'Label Predicted By RNN')
# # plt.axis([0, len(real_label) + 1, -1.5, 1.5])
# # plt.title('Label Prediction')
# # plt.xlabel('Time')
# # plt.ylabel('Retransmission Signal')
# # plt.legend()
# # plt.show()
# #
# # plt.figure(4)
# # predicted_label_plot_y1 = []
# # predicted_label_plot_x1 = []
# # for i, v in enumerate(predicted_label):
# #     if v + 0.3 >= 0:
# #         predicted_label_plot_y1.append([1])
# #         predicted_label_plot_x1.append([i])
# #     else:
# #         predicted_label_plot_y1.append([-1])
# #         predicted_label_plot_x1.append([i])
# # plt.plot(predicted_label_plot_x1, predicted_label_plot_y1, color = 'yellow', label = 'Corrected Label Predicted By RNN')
# # plt.axis([0, len(real_label) + 1, -1.5, 1.5])
# # plt.title('Label Prediction')
# # plt.xlabel('Time')
# # plt.ylabel('Retransmission Signal')
# # plt.legend()
# # plt.show()
# # n = 0
# # for i, v in enumerate(predicted_label_plot_y1):
# #     if v == real_label[i][0]:
# #         n += 1
# # fitting_rate1 = n/len(real_label)
#
# # plt.figure(5)
# predicted_label_plot_y2 = []
# predicted_label_plot_x2 = []
# for i, v in enumerate(predicted_label):
#     if v[0] < -0.5:
#         predicted_label_plot_y2.append([-1])
#         predicted_label_plot_x2.append([i])
#     else:
#         predicted_label_plot_y2.append([1])
#         predicted_label_plot_x2.append([i])
# #
# # for i in range(120, 140):
# #     predicted_label_plot_y2[i] = [1]
# #
# # #
# # for i in range(260, 290):
# #     predicted_label_plot_y2[i] = [1]
# #
# # for i in range(390, 410):
# #     predicted_label_plot_y2[i] = [1]
# #
# # #
# # plt.figure(1)
# plt.plot(predicted_label_plot_x2, predicted_label_plot_y2, color = 'green', label = 'Transmission Labels Predicted By LSTM')
# plt.axis([0, len(real_label) + 1, -1.5, 1.5])
# plt.title('Label Prediction')
# plt.xlabel('Time')
# plt.ylabel('Predicted Transmission Labels')
# plt.legend()
# plt.show()
# #
# # # for i, v in enumerate(predicted_label_plot_y2):
# # #     if v == real_label[i][0]:
# # #         n += 1
# # # fitting_rate2 = n/len(real_label)
# # real_label_total, index0 = cal_label(v_get_label, 0.3)
# # real_label = real_label_total[1000:1500]
# n = 0
# for i, v in enumerate(predicted_label_plot_y2):
#     if v[0] == -1:
#         n += 1
# r = n/len(predicted_label_plot_y2)
#
# m = 0
# for i, v in enumerate(pd_label):
#     if v[0] == -1:
#         m += 1
# r1 = m/len(pd_label)
# #
# # plt.figure(2)
# real_v_transmitted = scale_v(inputs_v_x[time_step:][:], inputs_v_y[time_step:][:], inputs_v_z[time_step:][:], real_label)
# real_v_scaled = scale_v(inputs_v_x[time_step:][:], inputs_v_y[time_step:][:], inputs_v_z[time_step:][:], real_label)
# predicted_v_transmitted = np.array(scale_v(inputs_v_x[time_step:][:], inputs_v_y[time_step:][:], inputs_v_z[time_step:][:], predicted_label_plot_y2)).transpose()
# pd_v_transmitted = np.array(scale_v(inputs_v_x[time_step:][:], inputs_v_y[time_step:][:], inputs_v_z[time_step:][:], pd_label)).transpose()
# real_v_x_transmitted, real_v_y_transmitted, real_v_z_transmitted = scale_v(inputs_v_x[time_step:][:], inputs_v_y[time_step:][:], inputs_v_z[time_step:][:], real_label)
# predicted_v_x_transmitted, predicted_v_y_transmitted, predicted_v_z_transmitted = scale_v(inputs_v_x[time_step:][:], inputs_v_y[time_step:][:], inputs_v_z[time_step:][:], predicted_label_plot_y2)
# pd_v_x_transmitted, pd_v_y_transmitted, pd_v_z_transmitted = scale_v(inputs_v_x[time_step:][:], inputs_v_y[time_step:][:], inputs_v_z[time_step:][:], pd_label)
# # real_v_transmitted, predicted_v_transmitted = [], []
# # for i, v in enumerate(real_v_x_transmitted):
# #     a = [v, real_v_y_transmitted[i], real_v_z_transmitted[i]]
# #     b = [predicted_v_x_transmitted[i], predicted_v_y_transmitted[i], predicted_v_z_transmitted[i]]
# #     real_v_transmitted.append(a)
# #     predicted_v_transmitted.append(b)
# # inputs = np.array(inputs0)
# hpw_real = hpw_psnr(inputs[time_step:], real_v_transmitted, 0.1, 1)
# hpw_predicted = hpw_psnr(inputs[time_step:], predicted_v_transmitted, 0.1, 1)
# hpw_pd = hpw_psnr(inputs[time_step:], pd_v_transmitted, 0.1, 1)
# # np.save('ld-hpw-lstm', hpw_predicted)
# # np.save('ld-hpw-pdcodecs', hpw_real)
# # x = range(0, 500)
# #
# # plt.scatter(x, hpw_predicted, color = 'blue', label = 'LSTM-based Model')
# # plt.scatter(x, hpw_real, color = 'red', marker='o', label = 'PD-Based Codecs')
# # plt.title('Comparison of HPW-PSNR for Force Signal')
# # plt.xlabel('Time ms')
# # plt.ylabel('HPW-PSNR dB')
# # plt.legend()
# # plt.show()
#
# # fitting_rate = jnd(inputs_v_x[time_step:][:], inputs_v_y[time_step:][:], inputs_v_z[time_step:][:], predicted_label_plot_y2, 0.1)
# # plt.plot(predicted_label_plot_x2, real_v_z_transmitted, color = 'red', label = 'Real Force Measured by Chai3d')
# # plt.plot(predicted_label_plot_x2, predicted_v_z_transmitted, color = 'blue', label = 'Transmitted Force Predicted By LSTM')
# # plt.plot(predicted_label_plot_x2, pd_v_z_transmitted, color = 'blue', label = 'Transmitted Force Predicted By PD-based Codecs')
# # plt.plot(predicted_label_plot_x2, real_v_transmitted, color = 'red', label = 'Real Transmitted Velocity')
# # plt.plot(predicted_label_plot_x2, real_v_z_transmitted, color = 'red', label = 'Real Force Measured by Chai3d')
# # equal_x, equal_y = [], []
# # for i, v in enumerate(real_v_z_transmitted):
# #     if v == predicted_v_z_transmitted[i]:
# #         equal_x.append(i)
# #         equal_y.append(v)
# # equal_x_plot, equal_y_plot = [], []
# # x, y = [], []
# # for i in range(0, len(equal_x) - 1):
# #     if equal_x[i + 1] - equal_x[i] == 1:
# #         x.append(equal_x[i])
# #         y.append(equal_y[i])
# #     else:
# #         x.append(equal_x[i])
# #         y.append(equal_y[i])
# #         equal_x_plot.append(x)
# #         equal_y_plot.append(y)
# #         x, y = [], []
# # equal_x_plot.append(x)
# # equal_y_plot.append(y)
# # for i, v in enumerate(equal_x_plot):
# #     plt.plot(v, equal_y_plot[i], color = 'purple')
#
# # equal_x_pd, equal_y_pd = [], []
# # for i, v in enumerate(real_v_z_transmitted):
# #     if v == pd_v_z_transmitted[i]:
# #         equal_x_pd.append(i)
# #         equal_y_pd.append(v)
# # equal_x_plot_pd, equal_y_plot_pd = [], []
# # x, y = [], []
# # for i in range(0, len(equal_x_pd) - 1):
# #     if equal_x_pd[i + 1] - equal_x_pd[i] == 1:
# #         x.append(equal_x_pd[i])
# #         y.append(equal_y_pd[i])
# #     else:
# #         x.append(equal_x_pd[i])
# #         y.append(equal_y_pd[i])
# #         equal_x_plot_pd.append(x)
# #         equal_y_plot_pd.append(y)
# #         x, y = [], []
# # equal_x_plot_pd.append(x)
# # equal_y_plot_pd.append(y)
# # for i, v in enumerate(equal_x_plot_pd):
# #     plt.plot(v, equal_y_plot_pd[i], color = 'purple')
# #
# #
# # plt.axis([0, len(predicted_label_plot_x2), min(real_v_z_transmitted) - 1, max(real_v_z_transmitted) + 1])
# # plt.title('Transmitted&Real Force Comparison')
# # plt.xlabel('Time')
# # plt.ylabel('Force')
# # plt.legend()
# # plt.show()
