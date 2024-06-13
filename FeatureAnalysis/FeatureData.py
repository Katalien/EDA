import pandas as pd
from typing import List, Dict


class FeatureData:
    def __init__(self, feature_name: str, data: Dict[str, List[float]],
                 min: float = None, max: float = None,
                 mean: float = None, std: float = None):
        self.feature_name = feature_name
        self.data = data
        self.min = min
        self.max = max
        self.mean = mean
        self.std = std