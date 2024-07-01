import matplotlib.pyplot as plt
from typing import List
from .Visualizer import Visualizer
from FeatureAnalysis import FeatureData
from DatasetProcessor import FeatureSummary

class LinePlotVisualizer(Visualizer):
    def visualize(self, feature_summary: FeatureSummary, grid=True):
        feature_data_list = feature_summary.features_list
        num_features = len(feature_data_list)

        if num_features == 1:
            fig, ax = plt.subplots(1, 1, figsize=(8, 6))
            axes = [ax]
        else:
            fig, axes = plt.subplots(1, num_features, figsize=(12, 6))

        for i, feature_data in enumerate(feature_data_list):
            if 'class' in feature_data.data.columns:
                # Второй тип данных с классом
                classes = feature_data.data['class'].unique()
                for cls in classes:
                    data_cls = feature_data.data[feature_data.data['class'] == cls]
                    axes[i].plot(data_cls['x'], data_cls['y'], label=f"{feature_data.feature_name} - {cls}")
            else:
                # Первый тип данных без класса
                print("x", list(feature_data.data['x']))
                # print("y", feature_data.data['y'])
                # print()
                axes[i].plot(feature_data.data['x'], feature_data.data['y'], label=feature_data.feature_name)

            axes[i].set_title(feature_data.feature_name)
            if grid:
                axes[i].grid(True)
            axes[i].legend()

        fig.suptitle("Line Plot of Feature Data", fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
        return fig