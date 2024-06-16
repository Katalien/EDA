import matplotlib.pyplot as plt
from .Visualizer import Visualizer
from typing import List
from FeatureAnalysis import FeatureData
import seaborn as sns

class DensityPlotVisualizer(Visualizer):
    def visualize(self, feature_data_list: List[FeatureData], grid=True):
        plt.figure(figsize=(12, 12))

        for feature_data in feature_data_list:
            y = feature_data.data["y"]
            sns.kdeplot(y, label=feature_data.feature_name, fill=True)

        plt.title("KDE Plot")
        if grid:
            plt.grid(True)
        plt.legend()
        # plt.show()
        return plt.gcf()