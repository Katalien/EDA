import cv2
import numpy as np
from FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.ClassFeatureData import ClassFeatureData
from DatasetProcessor import DatasetInfo
from ... import FeatureSummary
from typing import Dict, List
from .AtributesFeatures import AtributesFeatures

class Class2ImageRatioAnalysis(AtributesFeatures):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.image_size = dataset_info.image_size
        self.image_square = self.image_size[0] * self.image_size[1]
        self.feature_name = "Square 2 Image size Ratio"


    def _process_one_sample(self, sample: np.ndarray,  class_name:str):
        contours, _ = cv2.findContours(sample, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            ratio = area / self.image_square
            if str(class_name) not in list(self.classes_attr_dict.keys()):
                self.classes_attr_dict[class_name] = [ratio]
            else:
                self.classes_attr_dict[class_name].append(ratio)

    def get_feature(self) -> FeatureSummary:
        super().get_feature()
        self.summary.set_description("Ratio between classes square and image size")
        return self.summary

