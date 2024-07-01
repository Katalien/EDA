import os
import json
import cv2
import numpy as np
from FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.FeatureData import FeatureData
from DatasetProcessor import DatasetInfo
from .LabeledFeatures import LabeledFeatures

# общее количество всех классов в датасете
class ClassesSquareAnalysis(LabeledFeatures):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.feature_name = "Classes square"

    def _process_one_sample(self, sample: np.ndarray,  class_name:str):
        contours, _ = cv2.findContours(sample, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        num_segments = len(contours)

        if str(class_name) in list(self.classes_frequency.keys()):
            self.classes_frequency[class_name] += num_segments
        else:
            self.classes_frequency[class_name] = num_segments







