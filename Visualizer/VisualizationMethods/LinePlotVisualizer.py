import matplotlib.pyplot as plt
from .Visualizer import Visualizer
from FeatureAnalysis import FeatureData

class LinePlotVisualize(Visualizer):
    def visualize(self, feature_data, grid=True):
        plt.figure(figsize=(12, 12))
        for key in feature_data.data:
            x = feature_data.data[key]["x"]
            y = feature_data.data[key]["y"]
            plt.plot(x, y, label=key)
        plt.title(feature_data.feature_name)
        if grid:
            plt.grid(True)
        plt.legend()
        plt.show()
        return plt.gcf()
