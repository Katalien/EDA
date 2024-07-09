from DatasetProcessor import DatasetInfo
from .ImagesFeatures import ImagesFeatures
from ... import FeatureSummary
import numpy as np
import cv2


class ContrastAnalysis(ImagesFeatures):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.feature_name = "Contrast"


    def _process_one_sample(self, sample: np.ndarray):
        sample = cv2.cvtColor(sample, cv2.COLOR_BGR2GRAY)
        return np.std(sample)

    def get_feature(self) -> FeatureSummary:
        super().get_feature()
        self.summary.set_description("Overall contrast for all images in the dataset")
        return self.summary

