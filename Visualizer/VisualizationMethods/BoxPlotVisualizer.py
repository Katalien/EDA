import matplotlib.pyplot as plt
from .Visualizer import Visualizer

class BoxPlotVisualize(Visualizer):
    def visualize(self, feature_data, title, x_axis, y_axis):
        plt.figure(figsize=(8, 6))
        plt.boxplot(feature_data)
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title(title)
        plt.grid(True)
        return plt.gcf()