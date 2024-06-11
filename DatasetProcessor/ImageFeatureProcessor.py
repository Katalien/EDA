# обрабатывает одну метрику для одного изображения

import numpy as np
from typing import Type
from FeatureAnalysis import FeatureAnalysis

# class ImageFeatureProcessor:
#     def __init__(self, feature_processor:Type[FeatureAnalysis]):
#         self.feature_processor = feature_processor
#
#     def analyze(self, image: np.ndarray):
#         return self.feature_processor.extract(image)

class ImageFeatureProcessor:
    @staticmethod
    def analyze(feature_processor: Type[FeatureAnalysis], image: np.ndarray):
        return feature_processor.extract(image)
