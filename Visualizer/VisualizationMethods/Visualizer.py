from FeatureSummaryData import FeatureSummary


class Visualizer:
    """
    Class for visualizing features. Each class descendant represents a specific method for visualization
    """
    def visualize(self, feature_summary: FeatureSummary):
        raise NotImplementedError("Subclasses must implement visualize method")