import matplotlib.pyplot as plt
from .Visualizer import Visualizer
from FeatureSummaryData import FeatureSummary


class LinePlotVisualizer(Visualizer):
    def visualize(self, feature_summary: FeatureSummary, grid=True):
        feature_data_list = feature_summary.features_list
        visual_settings = feature_summary.visual_settings

        num_plots = len(feature_data_list)
        fig, axes = plt.subplots(num_plots, 1, figsize=(12, 4 * num_plots), sharex=True)

        if num_plots == 1:
            axes = [axes]

        if visual_settings and visual_settings.colors:
            colors = visual_settings.colors
        else:
            colors = plt.get_cmap('tab10').colors

        for idx, (ax, feature_data) in enumerate(zip(axes, feature_data_list)):
            x = feature_data.data["x"]
            y = feature_data.data["y"]
            color = colors[idx % len(colors)] if visual_settings and visual_settings.colors else None
            ax.plot(x, y, label=feature_data.class_name, color=color)
            subtitle = visual_settings.subtitles[
                idx] if visual_settings and visual_settings.subtitles else f"Line Plot of {feature_data.class_name}"
            ax.set_title(subtitle, fontsize=16, fontweight='bold')

            x_label = visual_settings.x_axes if visual_settings and visual_settings.x_axes else 'X Axis'
            y_label = visual_settings.y_axes if visual_settings and visual_settings.y_axes else 'Y Axis'
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)

            if visual_settings and visual_settings.grid:
                ax.grid(True)
            else:
                ax.grid(False)

            ax.legend()

        if visual_settings and visual_settings.title:
            plt.suptitle(visual_settings.title, fontsize=20, fontweight='bold')

        plt.tight_layout()
        return plt.gcf()