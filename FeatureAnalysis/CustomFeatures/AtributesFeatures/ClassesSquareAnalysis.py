import cv2
import numpy as np
from FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.ClassFeatureData import ClassFeatureData
from DatasetProcessor import DatasetInfo
from ... import FeatureSummary
from typing import Dict, List
from .AtributesFeatures import AtributesFeatures

class ClassesSquareAnalysis(AtributesFeatures):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.feature_name = "Square"


    def _process_one_sample(self, sample: np.ndarray,  class_name:str):
        contours, _ = cv2.findContours(sample, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if str(class_name) not in list(self.classes_attr_dict.keys()):
                self.classes_attr_dict[class_name] = [area]
            else:
                self.classes_attr_dict[class_name].append(area)

    def get_feature(self) -> FeatureSummary:
        super().get_feature()
        self.summary.set_description("Square of classes segments")
        return self.summary

