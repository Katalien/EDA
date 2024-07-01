import cv2
from abc import abstractmethod
import numpy as np
from FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.ClassFeatureData import ClassFeatureData
from DatasetProcessor import DatasetInfo
from typing import Dict, List

class AtributesFeatures(FeatureAnalysis):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.dataset_info = dataset_info
        self.classes_attr_dict: Dict[str, List] = {}
        self.featuresData = []
        self.feature_name = None

    def _process_dataset(self):
        file_dirs_dict = self.dataset_info.masks_path
        for i, (class_name, paths) in enumerate(file_dirs_dict.items()):
            for filepath in paths:
                image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
                self._process_one_sample(image, class_name)
        for class_name, data in self.classes_attr_dict.items():
            _min = min(data)
            _max = max(data)
            _mean = sum(data) / len(data)
            _std = (sum((x - _mean) ** 2 for x in data) / len(data)) ** 0.5
            _data_dict = {"x": len(data), "y": data}
            _feature_name = f"{self.feature_name} {class_name}"
            feature = FeatureData(_feature_name, _data_dict, _min, _max, _mean, _std)
            self.featuresData.append(feature)

    @abstractmethod
    def _process_one_sample(self, sample: np.ndarray, class_name: str):
        pass

    def get_feature(self):
        self._process_dataset()
        return self.featuresData


