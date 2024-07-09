from ... import FeatureSummary
from .LabelesFeatures import LabelesFeatures
from DatasetProcessor import DatasetInfo
import cv2
import numpy as np


class InstancePerImageAnalysis(LabelesFeatures):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.feature_name = "Instance per image"


    #TODO находит лишние контуры как исправить
    def _process_one_sample(self, sample: np.ndarray, class_name: str):
        kernel = np.ones((22, 22), np.uint8)
        sample = cv2.morphologyEx(sample, cv2.MORPH_CLOSE, kernel)

        _contours, _ = cv2.findContours(sample, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = []
        for cont in _contours:
            if cv2.contourArea(cont) >= 5:
                contours.append(cont)
        num_segments = len(contours)

        if class_name not in self.data:
            self.data[class_name] = [num_segments]
        else:
            self.data[class_name].append(num_segments)


    def _fill_zeroes(self):
        max_len = -1
        for val in self.data.values():
            if len(val) > max_len:
                max_len = len(val)
        for key, val in self.data.items():
            if len(val) < max_len:
                val.extend([0] * (max_len - len(val)))


    def get_feature(self) -> FeatureSummary:
        super().get_feature()
        self.summary.set_description("Amount of classes instances per image")
        return self.summary



