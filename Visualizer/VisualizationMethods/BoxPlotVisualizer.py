import matplotlib.pyplot as plt
from .Visualizer import Visualizer
import seaborn as sns
import numpy as np
import pandas as pd


class BoxPlotVisualizer(Visualizer):
    def visualize(self, feature_summary, grid=True):
        feature_data_list = feature_summary.features_list
        plt.figure(figsize=(12, 12))
        mean_values = [np.mean(feature_data.data["y"]) for feature_data in feature_data_list]
        # Determine if the difference between mean values is greater than n orders of magnitude
        if max(mean_values) / min(mean_values) > 10:
            BoxPlotVisualizer.__visualize_in_different_axis(feature_data_list)
        else:
            BoxPlotVisualizer.__visualize_in_one_axis(feature_summary, feature_data_list)
        plt.tight_layout()
        return plt.gcf()

    @staticmethod
    def __visualize_in_different_axis(feature_data_list):
        num_plots = len(feature_data_list)
        fig, axes = plt.subplots(1, num_plots, figsize=(12, 6 * num_plots), sharex=True)
        for i, feature_data in enumerate(feature_data_list):
            data = []
            ax = axes[i] if num_plots > 1 else axes
            class_name = feature_data.class_name
            y_values = feature_data.data["y"]
            for y in y_values:
                data.append({'class': class_name, 'value': y})
            df = pd.DataFrame(data)

            sns.boxplot(x='class', y='value', ax=ax, data=df, color=sns.color_palette("husl", num_plots)[i])
            ax.set_title(f"Box Plot of {feature_data.feature_name}", fontsize=20, fontweight='bold')
            ax.set_xlabel('Feature', fontsize=18)
            ax.set_ylabel('Value', fontsize=18)
            ax.grid(True)

    @staticmethod
    def __visualize_in_one_axis(feature_summary, feature_data_list):
        data = []
        for feature_data in feature_data_list:
            class_name = feature_data.class_name
            y_values = feature_data.data["y"]
            for y in y_values:
                data.append({'class': class_name, 'value': y})
        df = pd.DataFrame(data)
        colors = sns.color_palette("husl", len(feature_data_list))  # Get a palette of colors
        ax = sns.boxplot(x='class', y='value', orient="v", hue='class', data=df, palette=colors)
        ax.set_title(f"Box Plot of {feature_summary.feature_name}", fontsize=20, fontweight='bold')
        ax.set_xlabel('Class', fontsize=18)
        ax.set_ylabel('Value', fontsize=18)
        ax.grid(True)
        plt.legend(title='Classes', loc='upper left',
                   labels=[feature_data.class_name for feature_data in feature_data_list])