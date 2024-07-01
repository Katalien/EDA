import matplotlib.pyplot as plt
from .Visualizer import Visualizer
from FeatureAnalysis import FeatureSummary
import seaborn as sns
import pandas as pd

class ViolinPlotVisualizer(Visualizer):
    def visualize(self, feature_summary: FeatureSummary, grid=True):
        feature_data_list = feature_summary.features_list
        plt.figure(figsize=(12, 12))
        data_dict = {feature_data.feature_name: feature_data.data["y"] for feature_data in feature_data_list}
        df = pd.DataFrame(data_dict)
        print()
        print(df.head())
        sns.violinplot(data=df, orient="h")
        plt.title("Box Plot of Feature Data")
        plt.xlabel('Feature')
        plt.ylabel('Value')

        if grid:
            plt.grid(True)

        plt.tight_layout()
        # plt.show()
        return plt.gcf()