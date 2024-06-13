import matplotlib.pyplot as plt
from .Visualizer import Visualizer
from FeatureAnalysis import FeatureData
import seaborn as sns
import pandas as pd

class BoxPlotVisualize(Visualizer):
    def visualize(self, feature_data: FeatureData, grid=True):
        plt.figure(figsize=(12, 12))
        data_dict = {key: feature_data.data[key]["y"] for key in feature_data.data}
        df = pd.DataFrame(data_dict)
        sns.boxplot(data=df, orient="v")
        plt.title(feature_data.feature_name)
        plt.xlabel('Category')
        plt.ylabel('Value')
        if grid:
            plt.grid(True)
        plt.tight_layout()
        plt.show()
        return plt.gcf()