from typing import List
from FeatureAnalysis import FeatureData

class Visualizer:
    def visualize(self, feature_data: List[FeatureData]):
        raise NotImplementedError("Subclasses must implement visualize method")