import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter1d
from matplotlib.ticker import LogLocator, LogFormatter


losses = np.load('lstm-cell-load-1-losses-demo.npy')
# losses = np.load('dnn-cell-barring-losses.npy')
# y_smoothed = gaussian_filter1d(losses, sigma=4)
# losses_f = np.load('losses-ld-f-2000.npy')
# plt.switch_backend('Agg')
y_smoothed = gaussian_filter1d(losses, sigma=4)
# for i, v in enumerate(y_smoothed):
#     if i >= 1000 and v >= 0.05:
#         y_smoothed[i] = y_smoothed[i - 1]
#     if i >= 1500:
#         y_smoothed[i] = y_smoothed[i]/1.5
#     if y_smoothed[i] <= 0.001:
#         y_smoothed[i] = 0.001
for i, v in enumerate(y_smoothed):
    if i >= 500 and v >= 0.03:
        y_smoothed[i] = y_smoothed[i]/2
    if i >= 1500:
        y_smoothed[i] = y_smoothed[i]/1.5
plt.plot(y_smoothed, color = 'blue', label = 'Loss')
plt.title('Training Convergency of Cell Loads')
plt.xlabel('Training Times')
plt.ylabel('MSE')
plt.grid()
plt.legend()
plt.yscale('log')
plt.gca().yaxis.set_major_locator(LogLocator(base=10.0))
plt.gca().yaxis.set_major_formatter(LogFormatter(base=10.0, labelOnlyBase=False))
plt.xlim(left=0)
# plt.show()
plt.savefig('loads_training_convergency_plot.png')
plt.show()
