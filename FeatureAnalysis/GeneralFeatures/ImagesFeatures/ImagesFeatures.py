import cv2
from abc import abstractmethod
import numpy as np
from FeatureAnalysis import FeatureAnalysis, FeatureSummary
from FeatureAnalysis.ClassFeatureData import ClassFeatureData
from DatasetProcessor import DatasetInfo


class ImagesFeatures(FeatureAnalysis):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.path = self.dataset_info.images_path
        self.feature_name = None
        self.data = []
        self.mean = None
        self.min = None
        self.max = None
        self.std = None
        self.summary = None

    def _process_dataset(self):
        file_dirs = self.dataset_info.images_path
        for i, filepath in enumerate(file_dirs):
            image = cv2.imread(filepath)
            self.data.append(self._process_one_sample(image))
        self.min = min(self.data)
        self.max = max(self.data)
        self.mean = sum(self.data) / len(self.data)
        self.std = (sum((x - self.mean) ** 2 for x in self.data) / len(self.data)) ** 0.5

    @abstractmethod
    def _process_one_sample(self, sample: np.ndarray):
        pass

    @abstractmethod
    def get_feature(self) -> FeatureSummary:
        self._process_dataset()
        data_dict = {"x": len(self.data), "y": self.data}
        feature = ClassFeatureData(self.feature_name,
                                   data_dict,
                                   class_name="General",
                                   _min=self.min,
                                   _max=self.max,
                                   _mean=self.mean,
                                   _std=self.std)
        self.summary = FeatureSummary.FeatureSummary(self.feature_name, [feature], feature_tag="General")
        return self.summary
