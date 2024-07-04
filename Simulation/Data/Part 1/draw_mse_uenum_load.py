import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from matplotlib.ticker import LogLocator, LogFormatter

# Load the MSE data
mse_ue40 = np.load('lstm-cell-load-mse-ue40.npy')
mse_ue70 = np.load('lstm-cell-load-mse-ue70.npy')
mse_ue100 = np.load('lstm-cell-load-mse-ue100.npy')
mse_ue130 = np.load('lstm-cell-load-mse-ue130.npy')
mse_ue160 = np.load('lstm-cell-load-mse-ue160.npy')

# Smooth the losses
y_smoothed_ue40 = gaussian_filter1d(mse_ue40, sigma=4)
y_smoothed_ue70 = gaussian_filter1d(mse_ue70, sigma=4)
y_smoothed_ue100 = gaussian_filter1d(mse_ue100, sigma=4)
y_smoothed_ue130 = gaussian_filter1d(mse_ue130, sigma=4)
y_smoothed_ue160 = gaussian_filter1d(mse_ue160, sigma=4)

# Prepare the data for plotting
x_values = [40, 70, 100, 130, 160]
mse_values = [mse_ue40, mse_ue70, mse_ue100, mse_ue130, mse_ue160]
# Plot the smoothed losses
# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(x_values, mse_values, marker='o', linestyle='-', color='b', label='MSE')

plt.title('MSE Between Real and Predicted Cell Load with Different UE Quantities in Each Cell')
plt.xlabel('UE Quantity')
plt.ylabel('MSE')
plt.yscale('log')
plt.grid(True)
plt.legend()

# Ensure the y-axis is correctly scaled and visible
plt.gca().yaxis.set_major_locator(LogLocator(base=10.0))
plt.gca().yaxis.set_major_formatter(LogFormatter(base=10.0, labelOnlyBase=False))

y_ticks = [7e-3, 6e-3, 1e-2, 2e-2, 1e-1]
plt.yticks(y_ticks, [f'{y:.0e}' for y in y_ticks])


plt.xlim(left=30, right=170)  # Adjust the x-axis limits to fit the UE quantities

# Show the plot
plt.show()

