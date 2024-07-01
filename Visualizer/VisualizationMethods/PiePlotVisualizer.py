from .Visualizer import Visualizer
from FeatureAnalysis import FeatureSummary


class PiePlotVisualizer(Visualizer):
    def visualize(self, feature_summary: FeatureSummary, grid=True):
        feature_data_list = feature_summary.features_list