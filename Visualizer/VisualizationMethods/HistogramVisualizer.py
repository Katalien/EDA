import matplotlib.pyplot as plt
from .Visualizer import Visualizer


class HistogramVisualize(Visualizer):
    def visualize(self, feature_data, title, x_axis, y_axis, bins=10):
        plt.figure(figsize=(8, 6))
        plt.hist(feature_data, bins=bins)
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title(title)
        plt.grid(True)
        return plt.gcf()