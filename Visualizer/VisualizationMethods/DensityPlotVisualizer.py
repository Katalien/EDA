import matplotlib.pyplot as plt
from .Visualizer import Visualizer
from FeatureAnalysis import FeatureData
import seaborn as sns

class DensityPlotVisualize(Visualizer):
    def visualize(self, feature_data, grid=True):
        plt.figure(figsize=(12, 12))
        for key in feature_data.data:
            y = feature_data.data[key]["y"]
            sns.kdeplot(y, label=key, fill=True)
        plt.title(feature_data.feature_name)
        if grid:
            plt.grid(True)
        plt.legend()
        plt.show()
        return plt.gcf()