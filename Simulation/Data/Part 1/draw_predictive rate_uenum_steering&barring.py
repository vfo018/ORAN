import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from matplotlib.ticker import LogLocator, LogFormatter

# Load data
barring_ue40 = np.load('dnn-cell-barring-barring-predictive rate-ue40.npy')
steering_ue40 = np.load('dnn-cell-barring-steering-predictive rate-ue40.npy')
barring_ue70 = np.load('dnn-cell-barring-barring-predictive rate-ue70.npy')
steering_ue70 = np.load('dnn-cell-barring-steering-predictive rate-ue70.npy')
barring_ue100 = np.load('dnn-cell-barring-barring-predictive rate-ue100.npy')
steering_ue100 = np.load('dnn-cell-barring-steering-predictive rate-ue100.npy')
barring_ue130 = np.load('dnn-cell-barring-barring-predictive rate-ue130.npy')
steering_ue130 = np.load('dnn-cell-barring-steering-predictive rate-ue130.npy')
barring_ue160 = np.load('dnn-cell-barring-barring-predictive rate-ue160.npy')
steering_ue160 = np.load('dnn-cell-barring-steering-predictive rate-ue160.npy')

# Smooth the losses
sigma = 4
barring_ue40_smoothed = gaussian_filter1d(barring_ue40, sigma=sigma)
steering_ue40_smoothed = gaussian_filter1d(steering_ue40, sigma=sigma)
barring_ue70_smoothed = gaussian_filter1d(barring_ue70, sigma=sigma)
steering_ue70_smoothed = gaussian_filter1d(steering_ue70, sigma=sigma)
barring_ue100_smoothed = gaussian_filter1d(barring_ue100, sigma=sigma)
steering_ue100_smoothed = gaussian_filter1d(steering_ue100, sigma=sigma)
barring_ue130_smoothed = gaussian_filter1d(barring_ue130, sigma=sigma)
steering_ue130_smoothed = gaussian_filter1d(steering_ue130, sigma=sigma)
barring_ue160_smoothed = gaussian_filter1d(barring_ue160, sigma=sigma)
steering_ue160_smoothed = gaussian_filter1d(steering_ue160, sigma=sigma)

# Prepare the data for plotting
ue_quantities = [40, 70, 100, 130, 160]
barring_accuracy = [barring_ue40_smoothed, barring_ue70_smoothed, barring_ue100_smoothed, barring_ue130_smoothed, barring_ue160_smoothed]
steering_accuracy = [steering_ue40_smoothed, steering_ue70_smoothed, steering_ue100_smoothed, steering_ue130_smoothed, steering_ue160_smoothed]

# Plot the accuracy vs UE quantities
plt.figure(figsize=(10, 6))

plt.plot(ue_quantities, barring_accuracy, marker='o', linestyle='-', color='b', label='Cell Barring Accuracy')
plt.plot(ue_quantities, steering_accuracy, marker='o', linestyle='-', color='r', label='Traffic Steering Accuracy')

plt.title('Accuracy vs UE Quantity')
plt.xlabel('UE Quantity')
plt.ylabel('Accuracy')
plt.ylim(0, 1.1)  # Ensure y-axis range is between 0 and 1
plt.xticks(ue_quantities)
plt.grid(True)
plt.legend()

# Show the plot
plt.show()
# Or save the plot
# plt.savefig('accuracy_vs_ue_quantity.png')