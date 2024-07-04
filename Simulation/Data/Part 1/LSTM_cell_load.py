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
from keras.callbacks import EarlyStopping
from sklearn.metrics import mean_squared_error
#
#
#
#
my_data = pd.read_table('output_handover_scenario_training_UE40_cleaned.csv', sep=',')
cell_load = my_data.iloc[0:, 7:8].values
#
# #LSTM Nextwork
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
#
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
# # early_stopping = LambdaCallback(on_epoch_end=lambda epoch, logs: regressor.stop_training if logs['loss'] < 1e-4 else None)
# early_stopping = EarlyStopping(monitor='loss', patience=100, restore_best_weights=True)
#
# # Fitting the RNN to the Training set
# history = regressor.fit(X_train, y_train, epochs=10000, batch_size=1000, callbacks=[early_stopping])
# losses = history.history['loss']
# np.save('lstm-cell-load-losses-adam-ue40.npy', losses)
# regressor.save('lstm-cell-load-3-adam-ue40.keras')


regressor = load_model('lstm-cell-load-3-adam-ue40.keras')
test_data = pd.read_table('output_handover_scenario_testing_UE160_cleaned.csv', sep=',')
cell_load_test = test_data.iloc[0:, 7:8].values
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
mse = np.array([mean_squared_error(real_cell_load, regressor.predict(X_test))])
np.save('lstm-cell-load-mse-ue160.npy', mse)
real_cell_load = sc.inverse_transform(np.array(real_cell_load)).astype(int)
predicted_cell_load = np.round(sc.inverse_transform(regressor.predict(X_test))).astype(int)


# plt.figure(figsize=(14, 8))
# t = np.arange(len(real_cell_load))
# for i in range(CELL_NUMBER):
#     plt.plot(t, real_cell_load[:, i], label=f'Real Cell {i+1} Load')
#     plt.plot(predicted_cell_load[:, i], linestyle='--', label=f'Predicted Cell {i+1} Load')
#
# # matplotlib.use('Agg')
# plt.title('Real vs Predicted Cell Load')
# plt.xlabel('t')
# plt.ylabel('Cell Load')
# plt.legend()
# plt.show()
# plt.savefig('cell_load_comparison.png')

# fig, axs = plt.subplots(CELL_NUMBER, figsize=(14, 20))
#
# t = np.arange(300)  # Ensure t has the same length as the data arrays
#
# for i in range(CELL_NUMBER):
#     axs[i].plot(t, real_cell_load[:300, i], label=f'Real Cell {i+1} Load')
#     axs[i].plot(t, predicted_cell_load[:300, i], linestyle='--', label=f'Predicted Cell {i+1} Load')
#     axs[i].set_title(f'Cell {i+1} Load')
#     axs[i].set_xlabel('Time (t)')
#     axs[i].set_ylabel('Cell Load')
#     axs[i].legend()
#
# plt.tight_layout()
# plt.show()


