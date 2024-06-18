import matplotlib.pyplot as plt
from typing import List
from .Visualizer import Visualizer
from FeatureAnalysis import FeatureData
from DatasetProcessor import FeatureSummary


class PiePlotVisualizer(Visualizer):
    def visualize(self, feature_summary: FeatureSummary, grid=True):
        feature_data_list = feature_summary.features_list