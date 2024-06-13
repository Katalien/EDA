import matplotlib.pyplot as plt
from .Visualizer import Visualizer
from FeatureAnalysis import FeatureData

class BarPlotVisualize(Visualizer):
    def visualize(self, feature_data: FeatureData, grid=True):
        fig, axes = plt.subplots(1, len(feature_data.data.keys()), figsize=(10, 6))
        print(feature_data.data.items())
        for i, (key, values) in enumerate(feature_data.data.items()):
            x = feature_data.data[key]["x"]
            y = feature_data.data[key]["y"]
            axes[i].bar(x, y, label=key)
            if grid:
                axes[i].grid(True)
        fig.suptitle(feature_data.feature_name)
        plt.show()
        return plt.gcf()