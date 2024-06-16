import matplotlib.pyplot as plt
from typing import List
import numpy as np
from .Visualizer import Visualizer
from FeatureAnalysis import FeatureData


class BarPlotVisualizer(Visualizer):
    # def visualize(self, feature_data_list: List[FeatureData], grid=True):
    #     fig, axes = plt.subplots(1, len(feature_data_list), figsize=(10, 6))
    #
    #     for i, feature_data in enumerate(feature_data_list):
    #         x = list(feature_data.data["x"])
    #         y = list(feature_data.data["y"])
    #         axes[i].bar(x, y, label=feature_data.feature_name)
    #         axes[i].set_title(feature_data.feature_name)
    #         axes[i].set_xlabel('X')
    #         axes[i].set_ylabel('Y')
    #         if grid:
    #             axes[i].grid(True)
    #
    #     plt.suptitle("Bar plot of")
    #     plt.show()
    #     return plt.gcf()

    def visualize(self, feature_data_list: List[FeatureData], grid=True):
        fig, ax = plt.subplots(figsize=(10, 6))

        num_features = len(feature_data_list)
        bar_width = 0.3  # Ширина каждого столбца
        index = np.arange(len(feature_data_list[0].data["x"]))  # Индексы для каждой группы столбцов

        for i, feature_data in enumerate(feature_data_list):
            x = np.array(feature_data.data["x"])
            y = np.array(feature_data.data["y"])
            ax.bar(index + i * bar_width, y, bar_width, label=feature_data.feature_name)

        ax.set_title("Bar plot of Class Frequency")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_xticks(index + bar_width * (num_features - 1) / 2)  # Центрирование меток по оси x
        ax.set_xticklabels(feature_data_list[0].data["x"])  # Метки оси x
        if grid:
            ax.grid(True)

        plt.legend()
        plt.tight_layout()
        return fig