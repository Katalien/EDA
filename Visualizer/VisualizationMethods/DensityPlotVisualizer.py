import matplotlib.pyplot as plt
from .Visualizer import Visualizer
from typing import List
from FeatureAnalysis import FeatureData
from DatasetProcessor import FeatureSummary
import seaborn as sns

class DensityPlotVisualizer(Visualizer):
    def visualize(self, feature_summary: FeatureSummary, grid=True):
        feature_data_list = feature_summary.features_list
        plt.figure(figsize=(12, 12))

        for feature_data in feature_data_list:
            y = feature_data.data["y"]
            sns.kdeplot(y, label=feature_data.feature_name, fill=True)

        plt.title(f"KDE Plot of {feature_summary.feature_name}")
        if grid:
            plt.grid(True)
        plt.legend()
        # plt.show()
        return plt.gcf()