from keras.layers import Dropout
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM



my_data = pd.read_table('texture - LU - sliding - output.txt', sep=' ')
v_train = my_data.iloc[0:2000, 1:4].values
v_train_pca, vec = pca(v_train)
# print(vec)
# print(v_train_pca)

# vec_inv = np.matrix(vec).I
# m = np.dot(vec[:, 0:2], v_train_pca.T).T
# print(m)

#LSTM Nextwork
sc = MinMaxScaler(feature_range=(0, 1))
# vx_set_scaled = sc.fit_transform(v_train_pca[:, 0:1])
# vy_set_scaled = sc.fit_transform(v_train_pca[:, 1:2])
# vz_set_scaled = sc.fit_transform(v_train_pca[:, 2:3])
v_set_scaled = sc.fit_transform(v_train_pca[:, 0:3])
# v_z_set_scaled = sc.fit_transform(v_train_pca[:, 2:3])

time_step = 100
X_train = []
y_train = []
for i in range(time_step, 2000):
    X_train.append(v_set_scaled[i-time_step:i, 0:2])
    y_train.append(v_set_scaled[i - 1, 2])
X_train = np.array(X_train)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 2))
y_train = np.reshape(y_train, X_train.shape[0])

regressor = Sequential()
regressor.add(LSTM(units=100, return_sequences=True, input_shape=(X_train.shape[1], 2)))
regressor.add(Dropout(0.1))

regressor.add(LSTM(units=100, return_sequences=True))
regressor.add(Dropout(0.1))

regressor.add(LSTM(units=100, return_sequences=True))
regressor.add(Dropout(0.1))


regressor.add(LSTM(units=100))
regressor.add(Dropout(0.1))

# Adding the output layer
regressor.add(Dense(units=1))

# Compiling the RNN
regressor.compile(optimizer='adam', loss='mean_squared_error')

# Fitting the RNN to the Training set
regressor.fit(X_train, y_train, epochs=500, batch_size=100)


# Prediction
real_v = my_data.iloc[2000:3000, 1:4].values
# #
#
v_total = pd.concat((my_data.iloc[0:2000, 1:4], my_data.iloc[2000:3000, 1:4]), axis = 0)

# v_total_z = pd.concat((my_data.iloc[0:1000, 3:4], my_data.iloc[1000:2000, 3:4]), axis = 0)

inputs_v = v_total[len(v_total) - len(real_v) - time_step:].values
# v_test_pca, vec0 = pca(inputs_v)
# inputs_v = v_test_pca.reshape(-1, 3)
v_test_pca = np.dot(inputs_v, vec)
inputs_v = v_test_pca.reshape(-1, 3)
# inputs0 = sc.transform(inputs_v_x).tolist()
inputs_v = sc.transform(inputs_v)
X_test = []
for i in range(time_step, time_step + 1000):
    X_test.append(inputs_v[i-time_step:i, 0:2])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 2))
v_predict_reconstruct = regressor.predict(X_test)
# v_predict_reconstruct = sc.inverse_transform(np.append(inputs_v[60:, 0:2], v_predict_reconstruct, axis=1))
v_predict_reconstruct = sc.inverse_transform(np.append(inputs_v[time_step:, 0:2], v_predict_reconstruct, axis=1))
v_predict_reconstruct = eli_zero(v_predict_reconstruct, 2)
# t = sc.inverse_transform(inputs_v[time_step:, 0:3])
# v_predict_z_reconstruct = regressor.predict(X_test)
# v_predict_xy_reconstruct = sc.inverse_transform(inputs_v)[60:, 0:2]
# v_predict_z_reconstruct = sc.inverse_transform(np.append(inputs_v[60:, 0:2], v_predict_z_reconstruct, axis=1))[:, 2:3]
inputs_v_original = v_total[2000:3000].values
vec_inv = np.array(np.matrix(vec).I.tolist())
V_predict_reconstruct = np.dot(v_predict_reconstruct, vec_inv)
# V_predict_reconstruct0 = np.dot(vec0, v_predict_reconstruct.T).T
# PP = np.dot(v_predict_reconstruct[:, 0:2], vec0_inv[0:2, 0:2])
label = np.array(cal_label(inputs_v_original, V_predict_reconstruct, 0.2)).T
k = 0
for i, v in enumerate(label):
    if v == 1:
        k += 1
print(k/len(label))
