import matplotlib.pyplot as plt
from .Visualizer import Visualizer
from FeatureAnalysis import FeatureData


class HistogramVisualize(Visualizer):
    def visualize(self, feature_data: FeatureData, bins=10, grid=True):
        fig, axes = plt.subplots(1, len(feature_data.data.keys()), figsize=(12, 12))
        for i, (key, values) in enumerate(feature_data.data.items()):
            y = values["y"]
            axes[i].hist(y, bins=10, label=key)
            if grid:
                axes[i].grid(True)
        fig.suptitle(feature_data.feature_name)
        plt.show()
        return plt.gcf()
