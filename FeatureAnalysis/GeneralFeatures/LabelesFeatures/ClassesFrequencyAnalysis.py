import os
import json
import cv2
import numpy as np
from ... import FeatureSummary
from DatasetProcessor import DatasetInfo
from .LabelesFeatures import LabelesFeatures


# общее количество всех классов в датасете
class ClassesFrequencyAnalysis(LabelesFeatures):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.feature_name = "Classes frequency"

    def _process_one_sample(self, sample: np.ndarray,  class_name: str):
        contours, _ = cv2.findContours(sample, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        num_segments = len(contours)

        if str(class_name) in list(self.data.keys()):
            self.data[class_name] += num_segments
        else:
            self.data[class_name] = num_segments

    def get_feature(self) -> FeatureSummary:
        super().get_feature()
        self.summary.set_description("General amount of classes in dataset")
        return self.summary



