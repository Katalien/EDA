import matplotlib.pyplot as plt
from typing import List
from .Visualizer import Visualizer
from FeatureAnalysis import FeatureData

class ScatterPlotVisualizer(Visualizer):
    def visualize(self, feature_data_list: List[FeatureData], grid=True):
        plt.figure(figsize=(12, 12))
        for feature_data in feature_data_list:
            x = feature_data.data["x"]
            y = feature_data.data["y"]
            plt.scatter(x, y, label=feature_data.feature_name)
        plt.title("Scatter Plot of Feature Data")
        if grid:
            plt.grid(True)
        plt.legend()
        # plt.show()
        return plt.gcf()