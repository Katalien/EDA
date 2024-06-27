import cv2
from abc import abstractmethod
import numpy as np
from FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.FeatureData import FeatureData
from DatasetProcessor import DatasetInfo
import pandas as pd


class LabeledFeatures(FeatureAnalysis):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.dataset_info = dataset_info
        self.feature_name = None
        self.classes_frequency = {}

    def _process_dataset(self):
        file_dirs_dict = self.dataset_info.masks_path
        for i, (class_name, paths) in enumerate(file_dirs_dict.items()):
            for filepath in paths:
                image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
                self._process_one_sample(image, class_name)

    def get_feature(self):
        self._process_dataset()
        data_dict = {"x": list(self.classes_frequency.keys()), "y": list(self.classes_frequency.values())}
        feature = FeatureData(self.feature_name, data_dict)
        return feature