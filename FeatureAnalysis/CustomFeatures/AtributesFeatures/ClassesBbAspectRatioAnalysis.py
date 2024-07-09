import cv2
import numpy as np
from FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.ClassFeatureData import ClassFeatureData
from DatasetProcessor import DatasetInfo
from .AtributesFeatures import AtributesFeatures
from ... import FeatureSummary
from typing import Dict, List

class ClassesBbAspectRatioAnalysis(AtributesFeatures):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.feature_name = "Bounding box sides ratio"


    def _process_one_sample(self, sample: np.ndarray,  class_name:str):
        contours, _ = cv2.findContours(sample, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h
            if str(class_name) not in list(self.classes_attr_dict.keys()):
                self.classes_attr_dict[class_name] = [aspect_ratio]
            else:
                self.classes_attr_dict[class_name].append(aspect_ratio)

    def get_feature(self) -> FeatureSummary:
        super().get_feature()
        self.summary.set_description("Aspect ratio of classes bounging boxes")
        return self.summary

