from FeatureAnalysis.FeatureData import FeatureData
from DatasetProcessor import DatasetInfo
from .GeneralFeatures import GeneralFeatures
import numpy as np
import cv2
import pandas as pd


class BrightnessAnalysis(GeneralFeatures):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.feature_name = "Brightness"


    def _process_one_sample(self, sample: np.ndarray):
        return np.mean(sample)


