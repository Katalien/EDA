import numpy as np
from typing import List, Dict, Union
from FeatureAnalysis import FeatureAnalysis, FeatureSummary

# old
# Класс содержит информацию по определенной метрике для одного класса.
# Если метрика не прявязана к классу, то она имеет тег "General"
class ClassFeatureData:
    def __init__(self, feature_name: str,
                 data: List,
                 class_name: str = "General" ):
        self.feature_name: str = feature_name
        self.is_img: bool = False
        self.data: np.array = np.array(data)
        self.class_name: str = class_name
        self.min: float | int | None = None
        self.max: float | int | None  = None
        self.mean: float | int | None = None
        self.std: float | int | None  = None


