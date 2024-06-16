import matplotlib.pyplot as plt
from .Visualizer import Visualizer
from typing import List
from FeatureAnalysis import FeatureData
import seaborn as sns
import pandas as pd

class BoxPlotVisualizer(Visualizer):
    def visualize(self, feature_data_list: List[FeatureData], grid=True):
        plt.figure(figsize=(12, 12))
        data_dict = {feature_data.feature_name: feature_data.data["y"] for feature_data in feature_data_list}
        df = pd.DataFrame(data_dict)

        sns.boxplot(data=df, orient="v")
        plt.title("Box Plot of Feature Data")
        plt.xlabel('Feature')
        plt.ylabel('Value')

        if grid:
            plt.grid(True)

        plt.tight_layout()
        # plt.show()
        return plt.gcf()