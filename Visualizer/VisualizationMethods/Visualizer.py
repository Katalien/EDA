from typing import List
from FeatureAnalysis import FeatureData
from DatasetProcessor import FeatureSummary

class Visualizer:
    def visualize(self, feature_summary: FeatureSummary):
        raise NotImplementedError("Subclasses must implement visualize method")