from keras import Input
from keras.layers import Dropout
import numpy as np
# import matplotlib.pyplot as plt
import pandas as pd
from keras.src.layers import Flatten, Reshape
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from config import *
from keras.models import load_model
from keras.optimizers import Adam
from keras.optimizers import RMSprop
import matplotlib.pyplot as plt
from keras.callbacks import EarlyStopping
from keras.callbacks import LambdaCallback


my_data = pd.read_table('output_handover_scenario_training_UE40_cleaned.csv', sep=',')
cell_load = my_data.iloc[0:, 7:8].values.reshape(-1, 1)
cell_radius = my_data.iloc[0:, 12:13].values.reshape(-1, 1)
cell_barring = my_data.iloc[0:, 9:10].values
cell_steering = my_data.iloc[0:, 10:11].values
sc_load, sc_radius, sc_barring, sc_steering = (MinMaxScaler(feature_range=(0, 1)),
                                               MinMaxScaler(feature_range=(0, 1)), MinMaxScaler(feature_range=(0, 1)),
                                               MinMaxScaler(feature_range=(0, 1)))

cell_load_scaled = sc_load.fit_transform(cell_load)
cell_radius_scaled = sc_radius.fit_transform(cell_radius)
cell_barring_scaled = sc_barring.fit_transform(cell_barring)
cell_steering_scaled = sc_steering.fit_transform(cell_steering)

X_train, y_train = [], []
for i in range(0, len(cell_load_scaled) - CELL_NUMBER + 1, CELL_NUMBER):
    X_train.append(np.hstack((cell_load_scaled[i:i + CELL_NUMBER], cell_radius_scaled[i:i + CELL_NUMBER])))
    y_train.append(np.hstack((cell_barring_scaled[i:i + CELL_NUMBER], cell_steering_scaled[i:i + CELL_NUMBER])))

X_train = np.array(X_train)
y_train = np.array(y_train)

X_train = X_train.reshape((X_train.shape[0], CELL_NUMBER, 2))
y_train = y_train.reshape((y_train.shape[0], CELL_NUMBER, 2))

# print(cell_load_scaled)

#DNN Nextwork

#DNN Network
# regressor = Sequential()
# regressor.add(Input(shape=(CELL_NUMBER, 2)))
# regressor.add(Flatten())
# # Adding the first LSTM layer and some Dropout regularisation
# regressor.add(Dense(units=128, activation='relu'))
# regressor.add(Dropout(0.1))
# #
# # # Adding a second LSTM layer and some Dropout regularisation
# regressor.add(Dense(units=128, activation='relu'))
# regressor.add(Dropout(0.1))
# #
# # # Adding a third LSTM layer and some Dropout regularisation
#
# regressor.add(Dense(units=128, activation='relu'))
# regressor.add(Dropout(0.1))
#
# regressor.add(Dense(units=128, activation='relu'))
# regressor.add(Dropout(0.1))
# #
# # # Adding a fourth LSTM layer and some Dropout regularisation
# # regressor.add(Dense(units=y_train.shape[1]))
# regressor.add(Dense(units=CELL_NUMBER * 2))
# regressor.add(Reshape((CELL_NUMBER, 2)))
#
# optimizer = Adam(learning_rate=0.0001)
# regressor.compile(optimizer=optimizer, loss='mean_squared_error')
#
#
# # Define the stopping criterion
# early_stopping = LambdaCallback(on_epoch_end=lambda epoch, logs: regressor.stop_training if logs['loss'] < 1e-3 else None)
# # early_stopping = EarlyStopping(monitor='loss', patience=100, restore_best_weights=True)
#
# # history = regressor.fit(X_train, y_train, epochs=2000, batch_size=100, validation_split=0.2)
# history = regressor.fit(X_train, y_train, epochs= 20000, batch_size=100, callbacks=[early_stopping])
# # #
# #
# losses = history.history['loss']
# # # # val_losses = history.history['val_loss']
# np.save('dnn-cell-barring-steering-losses-ue40.npy', losses)
# regressor.save('dnn-cell-barring-steering-ue40.keras')
# print("Model trained and saved successfully.")

#
regressor = load_model('dnn-cell-barring-steering-ue40.keras')
test_data = pd.read_table('output_handover_scenario_testing_UE40_cleaned.csv', sep=',')
cell_load_test = test_data.iloc[0:, 7:8].values.reshape(-1, 1)
cell_radius_test = test_data.iloc[0:, 12:13].values.reshape(-1, 1)
cell_barring_test = test_data.iloc[0:, 9:10].values
cell_steering_test = test_data.iloc[0:, 10:11].values
cell_load_test = sc_load.transform(cell_load_test)
cell_radius_test = sc_radius.transform(cell_radius_test)
# cell_barring_test = sc_barring.transform(cell_barring_test)
# cell_steering_test = sc_steering.transform(cell_steering_test)
# #
# #
# # DNN Nextwork
X_test, real_barring_steering = [], []
for i in range(0, len(cell_load_test) - CELL_NUMBER + 1, CELL_NUMBER):
    X_test.append(np.hstack((cell_load_test[i:i + CELL_NUMBER], cell_radius_test[i:i + CELL_NUMBER])))
    real_barring_steering.append(np.hstack((cell_barring_test[i:i + CELL_NUMBER], cell_steering_test[i:i + CELL_NUMBER])))

real_barring_steering = np.array(real_barring_steering)
real_barring = real_barring_steering[:, :, 0:1]
real_steering = real_barring_steering[:, :, 1:2]
#
X_test = np.array(X_test)
real_barring_steering = np.array(real_barring_steering)
# # real_barring = sc.inverse_transform(np.array(real_barring))
predicted_barring_steering = regressor.predict(X_test)
# predicted_barring = predicted_barring_steering[:, :, 0:1]
# predicted_steering = predicted_barring_steering[:, :, 1:2]
predicted_barring = predicted_barring_steering[:, :, 0:1].reshape(-1, 1)
predicted_steering = predicted_barring_steering[:, :, 1:2].reshape(-1, 1)
# Reshape predictions to be 1D for inverse transform
predicted_barring = np.round(sc_barring.inverse_transform(predicted_barring)).astype(int)
predicted_steering = np.round(sc_steering.inverse_transform(predicted_steering)).astype(int)
predicted_rate_steering, predicted_rate_barring = 0, 0
m, n = 0, 0
for i, v in enumerate(predicted_steering):
    if v == cell_steering_test[i]:
        m += 1
    if predicted_barring[i] == cell_barring_test[i]:
        n += 1
predicted_rate_steering, predicted_rate_barring = m/len(predicted_steering), n/len(predicted_barring)
predicted_rate_steering, predicted_rate_barring = np.array([predicted_rate_steering]), np.array([predicted_rate_barring])
# np.save('dnn-cell-barring-steering-predictive rate-ue40.npy', predicted_rate_steering)
# np.save('dnn-cell-barring-barring-predictive rate-ue40.npy', predicted_rate_barring)

predicted_barring_steering = []
for i in range(0, len(cell_load_test) - CELL_NUMBER + 1, CELL_NUMBER):
    predicted_barring_steering.append(np.hstack((cell_barring_test[i:i + CELL_NUMBER], cell_steering_test[i:i + CELL_NUMBER])))
predicted_barring_steering = np.array(predicted_barring_steering)
predicted_barring = predicted_barring_steering[:, :, 0:1]
predicted_steering = predicted_barring_steering[:, :, 1:2]




# 分开画七张图
t = np.arange(300)
for i in range(CELL_NUMBER):
    # Plot barring
    plt.figure()
    plt.plot(real_barring[:300, i], label='Real Barring')
    plt.plot(predicted_barring[:300, i], linestyle='--', label='Predicted Barring')
    plt.title(f'Comparison of Real and LSTM Predicted Cell Barring for Cell {i + 1}')
    plt.xlabel('Time (t)')
    plt.ylabel('Cell Barring Label')
    plt.legend()
    plt.savefig(f'cell_{i + 1}_barring_comparison.png')
    plt.close()

    # Plot steering
    plt.figure()
    plt.plot(real_steering[:300, i], label='Real Steering')
    plt.plot(predicted_steering[:300, i], linestyle='--', label='Predicted Steering')
    plt.title(f'Comparison of Real and LSTM Predicted Traffic Steering for Cell {i + 1}')
    plt.xlabel('Time (t)')
    plt.ylabel('Traffic Steering Label')
    plt.legend()
    plt.savefig(f'cell_{i + 1}_steering_comparison.png')
    plt.close()


# predicted_barring = sc_barring.inverse_transform(predicted_barring_steering)
# predicted_steering = sc_barring.inverse_transform(predicted_barring_steering)[1]
# for i in range(0, len(predicted_barring)):
#     for j in rated_barring[i][j] < 0.5:
#             predicted_barring[i][j] = 0
#         else:
#             predicted_barring[i][j] = 1
#
#
# plt.figure(figsize=(14, 8))
# t = np.arange(0, 600)
# for i in range(CELL_NUMBER):
#     plt.plot(t, real_barring[:, i], label=f'Real Cell {i+1} Barring')
#     plt.plot(predicted_barring[:, i], linestyle='--', label=f'Predicted Cell {i+1} Barring')
#
# # matplotlib.use('Agg')
# plt.title('Real vs Predicted Cell Barring')
# plt.xlabel('t')
# plt.ylabel('Cell Barring')
# plt.legend()
# plt.show()
# plt.savefig('cell_Barring_comparison.png')


# Draw 7 subplots in 1 figure
# fig, axs = plt.subplots(CELL_NUMBER, 2, figsize=(15, 30))
# fig.suptitle('Predicted & Real Cell Barring and Traffic Steering Values', fontsize=20)
# t = np.arange(300)
#
# for i in range(CELL_NUMBER):
#     # Barring 图
#     axs[i, 0].plot(real_barring[:300, i], label='Real Barring')
#     axs[i, 0].plot(predicted_barring[:300, i], linestyle='--', label='Cell Barring Derived From DNN Model')
#     axs[i, 0].set_title(f'Cell {i+1} Barring')
#     axs[i, 0].set_xlabel('Time')
#     axs[i, 0].set_ylabel('Cell Barring Label')
#     axs[i, 0].legend()
#
#     # Steering 图
#     axs[i, 1].plot(real_steering[:300, i], label='Real Steering')
#     axs[i, 1].plot(predicted_steering[:300, i], linestyle='--', label='Traffic Steering Derived From DNN Model')
#     axs[i, 1].set_title(f'Cell {i+1} Traffic Steering')
#     axs[i, 1].set_xlabel('Time')
#     axs[i, 1].set_ylabel('Traffic Steering Label')
#     axs[i, 1].legend()
#
# plt.tight_layout(rect=[0, 0, 1, 0.96])
# plt.show()