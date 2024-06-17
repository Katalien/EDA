import numpy as np
import pandas as pd
from typing import List, Dict, Union


class FeatureData:
    def __init__(self, feature_name: str, data: Union[Dict[str, List[float]], np.ndarray],
                 min: float = None, max: float = None,
                 mean: float = None, std: float = None, is_img=False):
        self.feature_name = feature_name
        self.is_img = is_img
        self.data = data
        self.min = min
        self.max = max
        self.mean = mean
        self.std = std