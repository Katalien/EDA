import matplotlib.pyplot as plt
from .Visualizer import Visualizer
from FeatureAnalysis import FeatureSummary


class LinePlotVisualizer(Visualizer):
    def visualize(self, feature_summary: FeatureSummary, grid=True):
        feature_data_list = feature_summary.features_list
        plt.figure(figsize=(12, 12))
        for feature_data in feature_data_list:
            x = feature_data.data["x"]
            y = feature_data.data["y"]
            plt.plot(x, y, label=feature_data.feature_name)
        plt.title("Line Plot of Feature Data", fontsize=16, fontweight='bold')
        if grid:
            plt.grid(True)
        plt.legend()
        # plt.show()
        return plt.gcf()