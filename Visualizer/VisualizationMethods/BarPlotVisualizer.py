import matplotlib.pyplot as plt
from .Visualizer import Visualizer

class BarPlotVisualize(Visualizer):
    def visualize(self, feature_data):
        plt.bar(range(len(feature_data)), feature_data)
        plt.xlabel('Image Index')
        plt.ylabel('Feature Value')
        plt.title('Bar Plot')
        plt.show()