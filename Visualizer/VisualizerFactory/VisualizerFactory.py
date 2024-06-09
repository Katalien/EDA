from ..VisualizationMethods import LinePlotVisualizer
from ..VisualizationMethods import BarPlotVisualizer


class VisualizerFactory:
    @staticmethod
    def create_visualization_strategy(strategy_name):
        if strategy_name == 'line':
            return LinePlotVisualizer.LinePlotVisualize()
        elif strategy_name == 'bar':
            return BarPlotVisualizer.BarPlotVisualize()
        else:
            raise ValueError("Unknown visualization strategy")