import matplotlib.pyplot as plt
from .Visualizer import Visualizer
from FeatureAnalysis import FeatureData
from typing import List


class HistogramVisualizer(Visualizer):
    def visualize(self, feature_data_list: List[FeatureData], bins=10, grid=True):
        num_features = len(feature_data_list)

        if num_features == 1:
            fig, ax = plt.subplots(1, 1, figsize=(12, 12))
            axes = [ax]
        else:
            fig, axes = plt.subplots(1, num_features, figsize=(12, 12))

        for i, feature in enumerate(feature_data_list):
            x = feature.data["x"]
            y = feature.data["y"]
            axes[i].hist(y, bins=len(x), label=feature.feature_name)
            axes[i].set_title(feature.feature_name)
            if grid:
                axes[i].grid(True)
            axes[i].legend()

        fig.suptitle("Histogram")
        plt.tight_layout()
        plt.show()
        return plt.gcf()
