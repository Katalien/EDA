from .FeatureAnalysis import FeatureAnalysis
from PIL import Image
from .FeatureAnalysis import FeatureAnalysis
from .FeatureData import FeatureData
import numpy as np
import cv2
import os
import pandas as pd


class BrightnessAnalysis(FeatureAnalysis):
    def __init__(self, path: str):
        super().__init__(path)
        self.path = path
        self.feature_name = "Brightness"
        self.data = []
        self.mean = None
        self.min = None
        self.max = None
        self.std = None

    def _process_dataset(self):
        for file in os.listdir(self.path):
            image = cv2.imread(os.path.join(self.path, file))
            self.data.append(self._process_one_sample(image))
        self.min = min(self.data)
        self.max = max(self.data)
        self.mean = sum(self.data) / len(self.data)
        self.std = (sum((x - self.mean) ** 2 for x in self.data) / len(self.data)) ** 0.5

    def _process_one_sample(self, sample: np.ndarray):
        return np.mean(sample)

    def get_feature(self):
        self._process_dataset()
        data_dict = {"x": len(self.data), "y": self.data}
        df = pd.DataFrame(data_dict)
        feature = FeatureData(self.feature_name, df, self.min, self.max, self.mean, self.std)
        return feature
