import matplotlib.pyplot as plt
from typing import List
import numpy as np
from .Visualizer import Visualizer
from FeatureAnalysis import FeatureData
from DatasetProcessor import FeatureSummary


class BarPlotVisualizer(Visualizer):
    def visualize(self, feature_summary: FeatureSummary, grid=True):
        feature_data_list = feature_summary.features_list
        fig, ax = plt.subplots(figsize=(12, 12))

        num_features = len(feature_data_list)
        bar_width = 0.3  # Ширина каждого столбца
        index = np.arange(len(feature_data_list[0].data["x"]))  # Индексы для каждой группы столбцов

        for i, feature_data in enumerate(feature_data_list):
            x = np.array(feature_data.data["x"])
            y = np.array(feature_data.data["y"])
            ax.bar(index + i * bar_width, y, bar_width, label=feature_data.feature_name)

        ax.set_title(f"Bar Plot of {feature_summary.feature_name}", fontsize=16, fontweight='bold')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_xticks(index + bar_width * (num_features - 1) / 2)  # Центрирование меток по оси x
        ax.set_xticklabels(feature_data_list[0].data["x"])  # Метки оси x
        if grid:
            ax.grid(True)

        plt.legend()
        plt.tight_layout()
        return fig