import matplotlib.pyplot as plt
from .Visualizer import Visualizer

class BarPlotVisualize(Visualizer):
    def visualize(self, feature_data, title,  x_axis, y_axis, grid=True):
        plt.figure(figsize=(5, 5))
        plt.bar(range(len(feature_data)), feature_data, zorder=1)
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title(title)
        if grid:
            plt.grid(True, zorder=0)
        return plt.gcf()