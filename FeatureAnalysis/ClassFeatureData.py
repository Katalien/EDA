import numpy as np
from typing import List, Dict, Union


# Класс содержит информацию по определенной метрике для одного класса.
# Если метрика не прявязана к классу, то она имеет тег "General"
class ClassFeatureData:
    def __init__(self, feature_name: str,
                 data: Union[Dict[str, List[float]], np.ndarray, List],
                 class_name: str = "General",
                 _min: float | int = None,
                 _max: float | int = None,
                 _mean: float | int = None,
                 _std: float | int = None,
                 is_img: bool = False):
        self.feature_name: str = feature_name
        self.is_img: bool = is_img
        self.data: List = data
        self.class_name: str = class_name
        self.min: float | int = _min
        self.max: float | int = _max
        self.mean: float | int = _mean
        self.std: float | int = _std
