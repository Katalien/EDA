from ..VisualizationMethods import LinePlotVisualizer
from ..VisualizationMethods import BarPlotVisualizer
from ..VisualizationMethods import BoxPlotVisualizer
from ..VisualizationMethods import HistogramVisualizer
from ..VisualizationMethods import ScatterPlotVisualizer


class VisualizerFactory:
    @staticmethod
    def create_visualization_strategy(method):
        if method == 'line':
            return LinePlotVisualizer.LinePlotVisualize()
        elif method == 'bar':
            return BarPlotVisualizer.BarPlotVisualize()
        elif method == 'histogram':
            return HistogramVisualizer.HistogramVisualize()
        elif method == 'boxplot':
            return BoxPlotVisualizer.BoxPlotVisualize()
        elif method == 'scatter':
            return ScatterPlotVisualizer.ScatterPlotVisualize()
        else:
            raise ValueError("Unknown visualization strategy")