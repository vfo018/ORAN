from keras.layers import Dropout
import numpy as np
# import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from config import *
from keras.models import load_model
from keras.optimizers import Adam
from keras.optimizers import RMSprop
import matplotlib.pyplot as plt


my_data = pd.read_table('output_handover_scenario_training_UE40_cleaned.csv', sep=',')
cell_load = my_data.iloc[0:, 7:8].values
cell_barring = my_data.iloc[0:, 9:10].values
sc = MinMaxScaler(feature_range=(0, 1))

cell_load_scaled = sc.fit_transform(cell_load)
cell_barring_scaled = sc.fit_transform(cell_barring)

#DNN Nextwork
X_train, y_train = [], []
for i in range(0, len(cell_load_scaled) - CELL_NUMBER + 1, CELL_NUMBER):
    X_train.append(cell_load_scaled[i:i + CELL_NUMBER].flatten())
    y_train.append(cell_barring_scaled[i:i + CELL_NUMBER].flatten())

X_train = np.array(X_train)
y_train = np.array(y_train)

#DNN Network
regressor = Sequential()

# Adding the first LSTM layer and some Dropout regularisation
regressor.add(Dense(units=128, activation='sigmoid', input_dim=X_train.shape[1]))
regressor.add(Dropout(0.1))
#
# # Adding a second LSTM layer and some Dropout regularisation
regressor.add(Dense(units=128, activation='relu'))
regressor.add(Dropout(0.1))
#
# # Adding a third LSTM layer and some Dropout regularisation

regressor.add(Dense(units=128, activation='sigmoid'))
regressor.add(Dropout(0.1))

regressor.add(Dense(units=128, activation='relu'))
regressor.add(Dropout(0.1))
#
# # Adding a fourth LSTM layer and some Dropout regularisation
regressor.add(Dense(units=CELL_NUMBER))

optimizer = Adam(learning_rate=0.001)
regressor.compile(optimizer=optimizer, loss='mean_squared_error')

# history = regressor.fit(X_train, y_train, epochs=2000, batch_size=100, validation_split=0.2)
history = regressor.fit(X_train, y_train, epochs=10000, batch_size=100)


losses = history.history['loss']
# val_losses = history.history['val_loss']
np.save('dnn-cell-barring-losses.npy', losses)
regressor.save('dnn-cell-barring.keras')

# regressor = load_model('dnn-cell-barring-steering-ue40.keras')
# test_data = pd.read_table('output_handover_scenario_testing_UE40_cleaned.csv', sep=',')
# cell_load_test = test_data.iloc[0:4200, 7:8].values
# cell_barring_test = test_data.iloc[0:4200, 9:10].values
# cell_load_test = sc.transform(cell_load_test)
# cell_barring_test = sc.transform(cell_barring_test)


#DNN Nextwork
# X_test, real_barring = [], []
# for i in range(0, len(cell_load_test) - CELL_NUMBER + 1, CELL_NUMBER):
#     X_test.append(cell_load_test[i:i + CELL_NUMBER].flatten())
#     real_barring.append(cell_barring_scaled[i:i + CELL_NUMBER].flatten())
#
# X_test = np.array(X_test)
# real_barring = np.array(real_barring)
# real_barring = sc.inverse_transform(np.array(real_barring))
# predicted_barring = sc.inverse_transform(regressor.predict(X_test))
# for i in range(0, len(predicted_barring)):
#     for j in range(0, CELL_NUMBER):
#         if predicted_barring[i][j] < 0.5:
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