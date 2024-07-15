import cv2
import numpy as np
from FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.ClassFeatureData import ClassFeatureData
from DatasetProcessor import DatasetInfo
from FeatureAnalysis import FeatureSummary
from typing import Dict, List
from .AtributesFeatures import AtributesFeatures

class Class2ImageRatioAnalysis(AtributesFeatures):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.feature_name = "Defect area/image area"


    def _process_one_sample(self, sample: np.ndarray,  class_name:str):
        image_area = sample.shape[0] * sample.shape[1]
        contours, _ = cv2.findContours(sample, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area != 0:
                ratio = area / image_area
                if str(class_name) not in list(self.classes_attr_dict.keys()):
                    self.classes_attr_dict[class_name] = [ratio]
                else:
                    self.classes_attr_dict[class_name].append(ratio)

    def get_feature(self) -> FeatureSummary:
        super().get_feature()
        self.summary.set_description("The ratio of the defect area to the area of the entire image")
        return self.summary

