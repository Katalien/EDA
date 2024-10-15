import matplotlib.pyplot as plt
import numpy as np
from .Visualizer import Visualizer
from FeatureSummaryData import FeatureSummary


class BarPlotVisualizer(Visualizer):
    def visualize(self, feature_summary: FeatureSummary, grid=True):
        feature_data_list = feature_summary.features_list
        num_classes = len(feature_data_list)

        fig, ax = plt.subplots(figsize=(12, 12))

        bar_width = 0.8 / num_classes  # Ширина каждого столбца, нормализована по количеству классов
        index = np.arange(num_classes)  # Индексы для каждого класса

        y_values = [feature_data.data["y"] for feature_data in feature_data_list]
        class_names = [feature_data.class_name for feature_data in feature_data_list]

        colors = plt.get_cmap('tab10', num_classes)  # Получаем цветовую карту с 10 цветами

        for i in range(num_classes):
            ax.bar(index[i], y_values[i], bar_width, color=colors(i), label=class_names[i])

        ax.set_title(f"Bar Plot of {feature_summary.feature_name}", fontsize=16, fontweight='bold')
        ax.set_xlabel('Class')
        ax.set_ylabel('Y')

        if grid:
            ax.grid(True)

        ax.legend()
        plt.tight_layout()
        return fig
