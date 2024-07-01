from FeatureAnalysis import FeatureSummary


class Visualizer:
    def visualize(self, feature_summary: FeatureSummary):
        raise NotImplementedError("Subclasses must implement visualize method")