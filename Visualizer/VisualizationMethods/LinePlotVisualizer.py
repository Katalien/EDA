import matplotlib.pyplot as plt
from .Visualizer import Visualizer
from FeatureAnalysis import FeatureSummary


class LinePlotVisualizer(Visualizer):
    def visualize(self, feature_summary: FeatureSummary, grid=True):
        feature_data_list = feature_summary.features_list
        num_plots = len(feature_data_list)
        fig, axes = plt.subplots(num_plots, 1, figsize=(12, 4 * num_plots), sharex=True)

        if num_plots == 1:
            axes = [axes]

        for ax, feature_data in zip(axes, feature_data_list):
            x = feature_data.data["x"]
            y = feature_data.data["y"]
            ax.plot(x, y, label=feature_data.class_name)
            ax.set_title(f"Line Plot of {feature_data.class_name}", fontsize=16, fontweight='bold')
            if grid:
                ax.grid(True)
            ax.legend()

        plt.tight_layout()
        return plt.gcf()