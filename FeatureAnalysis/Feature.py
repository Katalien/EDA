import pandas as pd
from typing import List
from Visualizer import VisualizationParams

class FeatureData:
    def __init__(self, feature_name: str, data: pd.DataFrame, desc: str = ""):
        self.feature_name = feature_name
        self.data = data
        self.desc = desc
        self.visual_methods = []

    def set_visual_methods(self, methods: List[str]):
        self.visual_methods = methods
