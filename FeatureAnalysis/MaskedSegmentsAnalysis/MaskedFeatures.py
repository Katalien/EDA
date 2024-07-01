import cv2
from abc import abstractmethod
import numpy as np
from FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.FeatureData import FeatureData
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
        self.grayscale = None

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
        if self.grayscale:
            mask2merge = mask.copy()
        else:
            mask2merge = cv2.merge([mask, mask, mask])
        masked_image = cv2.bitwise_and(image, mask2merge, mask=mask)
        return masked_image

    def get_feature(self):
        self._process_dataset()
        dfs = []
        for class_name, values in self.data.items():
            df = pd.DataFrame({'x': range(1, len(values) + 1), 'y': values})
            df['class'] = class_name
            dfs.append(df)

        final_df = pd.concat(dfs, ignore_index=True)
        feature = FeatureData(self.feature_name, final_df, self.min, self.max, self.mean, self.std)
        return feature