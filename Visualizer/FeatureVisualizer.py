from .VisualizerFactory.VisualizerFactory import VisualizerFactory


class FeatureVisualizer:
    def __init__(self, feature_data):
        self.feature_data = feature_data

    def visualize(self, method, title, x_axis, y_axis):
        strategy = VisualizerFactory.create_visualization_strategy(method)
        return strategy.visualize(self.feature_data, title, x_axis, y_axis)