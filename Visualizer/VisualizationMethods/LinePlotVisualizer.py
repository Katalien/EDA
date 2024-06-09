import matplotlib.pyplot as plt
from .Visualizer import Visualizer

class LinePlotVisualize(Visualizer):
    def visualize(self, feature_data, title,  x_axis, y_axis, grid=True):
        plt.figure(figsize=(12, 12))
        x = range(len(feature_data))
        plt.plot(x, feature_data)
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title(title)
        if grid:
            plt.grid(True)
        return plt.gcf()
