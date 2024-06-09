from ..VisualizationMethods import LinePlotVisualizer
from ..VisualizationMethods import BarPlotVisualizer


class VisualizerFactory:
    @staticmethod
    def create_visualization_strategy(method):
        if method == 'line':
            return LinePlotVisualizer.LinePlotVisualize()
        elif method == 'bar':
            return BarPlotVisualizer.BarPlotVisualize()
        else:
            raise ValueError("Unknown visualization strategy")