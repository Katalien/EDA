import matplotlib.pyplot as plt
from .Visualizer import Visualizer
from FeatureAnalysis import FeatureData

class ScatterPlotVisualize(Visualizer):
    def visualize(self, feature_data: FeatureData, grid=True):
        plt.figure(figsize=(12, 12))
        for key in feature_data.data:
            x = feature_data.data[key]["x"]
            y = feature_data.data[key]["y"]
            plt.scatter(x, y, label=key)
        plt.title(feature_data.feature_name)
        if grid:
            plt.grid(True)
        plt.show()
        return plt.gcf()