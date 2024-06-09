from .VisualizerFactory.VisualizerFactory import VisualizerFactory


class FeatureVisualizer:
    def __init__(self, feature_data):
        self.feature_data = feature_data

    def visualize(self, strategy_name):
        strategy = VisualizerFactory.create_visualization_strategy(strategy_name)
        strategy.visualize(self.feature_data)