import pandas as pd
from Visualizer import VisualizationParams

class Feature:
    def __init__(self, feature_name: str, data:pd.DataFrame, visualization_params:VisualizationParams):
        self.feature_name = feature_name
        self.visualization_params = visualization_params
        self.visualization_params = visualization_params
        self.data = data
        self.desc = ""