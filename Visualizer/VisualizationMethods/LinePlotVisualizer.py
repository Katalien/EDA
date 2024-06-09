import matplotlib.pyplot as plt
from .Visualizer import Visualizer

class LinePlotVisualize(Visualizer):
    def visualize(self, feature_data):
        x = range(len(feature_data))
        plt.plot(x, feature_data)
        plt.xlabel('Image Index')
        plt.ylabel('Feature Value')
        plt.title('Line Plot')
        plt.show()