import matplotlib.pyplot as plt
from .Visualizer import Visualizer
from FeatureAnalysis import FeatureData


class PiePlotVisualize(Visualizer):
    def visualize(self, feature_data, grid=True):
        plt.figure(figsize=(12, 12))
        labels = []
        sizes = []
        for key in feature_data.data:
            labels.append(key)
            sizes.append(sum(feature_data.data[key]["y"]))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title(feature_data.feature_name)
        plt.axis('equal')
        plt.show()
        return plt.gcf()