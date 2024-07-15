import cv2
from abc import abstractmethod
import numpy as np
from FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.ClassFeatureData import ClassFeatureData
from FeatureAnalysis import FeatureSummary
from DatasetProcessor import DatasetInfo
from typing import Dict, List


class AtributesFeatures(FeatureAnalysis):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.dataset_info = dataset_info
        self.classes_attr_dict: Dict[str, List] = {}
        self.featuresData = []
        self.feature_name = None
        self.summary = None

    def _process_dataset(self):
        file_dirs_dict = self.dataset_info.masks_path
        for i, (class_name, paths) in enumerate(file_dirs_dict.items()):
            for filepath in paths:
                image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
                kernel = np.ones((5, 5), 'uint8')
                image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
                self._process_one_sample(image, class_name)
        for class_name, data in self.classes_attr_dict.items():
            _min = min(data)
            _max = max(data)
            _mean = sum(data) / len(data)
            _std = (sum((x - _mean) ** 2 for x in data) / len(data)) ** 0.5
            _data_dict = {"x": len(data), "y": data}
            feature = ClassFeatureData(self.feature_name,
                                       _data_dict,
                                       class_name=class_name,
                                       _min=_min,
                                       _max=_max,
                                       _mean=_mean,
                                       _std=_std)
            self.featuresData.append(feature)

    @abstractmethod
    def _process_one_sample(self, sample: np.ndarray, class_name: str):
        pass

    @abstractmethod
    def get_feature(self):
        self._process_dataset()
        self.summary = FeatureSummary.FeatureSummary(self.feature_name, self.featuresData, feature_tag="Attributes")
        return self.featuresData


