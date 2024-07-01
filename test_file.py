import cv2
from abc import abstractmethod
import numpy as np
from FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.FeatureData import FeatureData
from DatasetProcessor import DatasetInfo
import pandas as pd
from utils.utils import mask_path2image_path


class MaskedFeatures():
    def __init__(self):
        self.feature_name = None
        self.data = []
        self.mean = None
        self.min = None
        self.max = None
        self.std = None

    def process_dataset(self, grayscale=True):
        mask_path = "../dataset/real_dataset/56_skoli/face/01/01_top.tif"
        image_path = mask_path2image_path(mask_path)
        if grayscale:
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        else:
            image = cv2.imread(image_path)
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        self._get_masked_image(image, mask, grayscale)

    @abstractmethod
    def _process_one_sample(self, sample: np.ndarray, mask: np.ndarray):
        pass

    def _get_masked_image(self, image, mask, grayscale=True):
        if grayscale:
            mask2merge = mask.copy()
        else:
            mask2merge = cv2.merge([mask, mask, mask])
        masked_image = cv2.bitwise_and(image, mask2merge, mask=mask)
        image = cv2.resize(masked_image, (0, 0), fx=0.3, fy=0.3)
        cv2.imshow("", image)
        cv2.waitKey()

    def get_feature(self):
        self._process_dataset()
        data_dict = {"x": len(self.data), "y": self.data}
        df = pd.DataFrame(data_dict)
        feature = FeatureData(self.feature_name, df, self.min, self.max, self.mean, self.std)
        return feature


analyzer = MaskedFeatures()
analyzer.process_dataset()