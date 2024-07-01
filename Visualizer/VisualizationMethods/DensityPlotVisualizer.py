import matplotlib.pyplot as plt
from .Visualizer import Visualizer
from FeatureAnalysis import FeatureSummary
import seaborn as sns

class DensityPlotVisualizer(Visualizer):
    def visualize(self, feature_summary: FeatureSummary, grid=True):
        feature_data_list = feature_summary.features_list
        num_features = len(feature_data_list)

        fig, axes = plt.subplots(nrows=num_features, ncols=1, figsize=(12, 12))

        for i, feature_data in enumerate(feature_data_list):

            ax = axes[i] if num_features > 1 else axes  # Если только один subplot, используем его напрямую
            y = feature_data.data["y"]
            sns.kdeplot(y, label=feature_data.feature_name, fill=True, ax=ax)
            ax.set_title(f"KDE Plot of {feature_data.feature_name}")

            if grid:
                ax.grid(True)

            ax.legend()

        fig.suptitle(f"KDE Plots of {feature_summary.feature_name}", fontsize=16, fontweight='bold')
        plt.tight_layout()  # Улучшает автоматическое размещение subplot'ов

        return fig

    def visualize_one_plot(self, feature_summary: FeatureSummary, grid=True):
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