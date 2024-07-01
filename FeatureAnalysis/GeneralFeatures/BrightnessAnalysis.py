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

    def get_feature(self):
        self._process_dataset()
        data_dict = {"x": range(len(self.data)), "y": self.data}
        df = pd.DataFrame(data_dict)
        feature = FeatureData(self.feature_name, df, self.min, self.max, self.mean, self.std)
        return feature

