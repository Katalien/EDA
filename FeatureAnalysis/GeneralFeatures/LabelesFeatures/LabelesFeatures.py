import cv2
from abc import abstractmethod
from FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.ClassFeatureData import ClassFeatureData
from DatasetProcessor import DatasetInfo
from FeatureAnalysis import FeatureSummary
from typing import Any


class LabelesFeatures(FeatureAnalysis):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.dataset_info = dataset_info
        self.feature_name = None
        self.data = {}
        self.summary = None

    def _process_dataset(self):
        file_dirs_dict = self.dataset_info.masks_path
        for i, (class_name, paths) in enumerate(file_dirs_dict.items()):
            for filepath in paths:
                image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
                self._process_one_sample(image, class_name)

    @abstractmethod
    def _process_one_sample(self,  *args: Any, **kwargs: Any):
        pass

    @abstractmethod
    def get_feature(self) -> FeatureSummary:
        self._process_dataset()
        features = []
        for key, val in self.data.items():
            cur_class_freq = {"x": key, "y": val}
            cur_feature = ClassFeatureData(self.feature_name,
                                           cur_class_freq,
                                           class_name=key)
            features.append(cur_feature)
        self.summary = FeatureSummary.FeatureSummary(self.feature_name, features)
        return self.summary
