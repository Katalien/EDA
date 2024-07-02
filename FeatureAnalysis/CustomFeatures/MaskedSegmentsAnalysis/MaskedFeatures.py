import cv2
from abc import abstractmethod
import numpy as np
from FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.ClassFeatureData import ClassFeatureData
from ... import FeatureSummary
from DatasetProcessor import DatasetInfo
import pandas as pd
from typing import Dict, List
from utils.utils import mask_path2image_path


class MaskedFeatures(FeatureAnalysis):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.path = self.dataset_info.images_path
        self.feature_name = None
        self.data: Dict[str, List] = {}
        self.mean = None
        self.min = None
        self.max = None
        self.std = None
        self.summary: FeatureSummary = None

    def _process_dataset(self):
        for class_name, mask_filepaths in self.dataset_info.masks_path.items():
            self.data[class_name] = []
            for mask_path in mask_filepaths:
                image_path = mask_path2image_path(mask_path)
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
                self.data[class_name].extend(self._process_one_sample(image, mask))


    @abstractmethod
    def _process_one_sample(self, sample: np.ndarray, mask: np.ndarray):
        pass


    def _get_masked_image(self, image, mask):
        mask2merge = mask.copy()
        masked_image = cv2.bitwise_and(image, mask2merge, mask=mask)
        return masked_image

    def _count_stat_values(self, data):
        data_sorted = np.sort(data)

        Q1 = np.percentile(data_sorted, 25)
        Q3 = np.percentile(data_sorted, 75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        median = np.median(data_sorted)

        return lower_bound, upper_bound, median

    @abstractmethod
    def get_feature(self) -> FeatureSummary:
        self._process_dataset()
        features = []
        for class_name, values in self.data.items():
            cur_dict = {'x': range(1, len(values) + 1), 'y': values}

            _min = min(values)
            _max= max(values)
            _mean = sum(values) / len(values)
            _std = (sum((x - _mean) ** 2 for x in values) / len(values)) ** 0.5
            lower, upper, median = self._count_stat_values(values)
            stat_info = f"Lower boundary: {lower}\nUpper boundary: {upper}\nMedian: {median}"
            cur_feature = ClassFeatureData(self.feature_name,
                                           cur_dict,
                                           class_name=class_name,
                                           _min=min(values),
                                           _max=max(values),
                                           _mean=_mean,
                                           _std=_std,
                                           add_info=stat_info)
            features.append(cur_feature)
        self.summary = FeatureSummary.FeatureSummary(self.feature_name, features)

        return self.summary
