import matplotlib.pyplot as plt
from typing import List
from .Visualizer import Visualizer
from FeatureAnalysis import FeatureData

class BarPlotVisualizer(Visualizer):
    def visualize(self, feature_data_list: List[FeatureData], grid=True):
        fig, axes = plt.subplots(1, len(feature_data_list), figsize=(10, 6))

        for i, feature_data in enumerate(feature_data_list):
            x = feature_data.data["x"]
            y = feature_data.data["y"]
            axes[i].bar(x, y, label=feature_data.feature_name)
            axes[i].set_title(feature_data.feature_name)
            axes[i].set_xlabel('X')
            axes[i].set_ylabel('Y')
            if grid:
                axes[i].grid(True)

        plt.suptitle("Bar plot of")
        # plt.show()
        return plt.gcf()