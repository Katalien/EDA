import os
from FeatureAnalysis.FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.FeatureData import FeatureData
from DatasetProcessor import FileIterator
import numpy as np
import pandas as pd
import cv2


class ContrastAnalysis(FeatureAnalysis):
    def __init__(self, path: str):
        super().__init__(path)
        self.path = path
        self.feature_name = "Contrast"
        self.data = []
        self.mean = None
        self.min = None
        self.max = None
        self.std = None

    def _process_dataset(self):
        image_files, file_dirs = FileIterator.get_images_from_lowest_level_folders(self.path)
        for i, dir_path in enumerate(file_dirs):
            for image_name in os.listdir(dir_path):
                if len(image_name.split("_")) == 1:  # get original image
                    filepath = os.path.join(os.path.normpath(dir_path), image_name)
                    filepath = filepath.replace("\\", "/")
                    image = cv2.imread(filepath)
                    self.data.append(self._process_one_sample(image))
        self.min = min(self.data)
        self.max = max(self.data)
        self.mean = sum(self.data) / len(self.data)
        self.std = (sum((x - self.mean) ** 2 for x in self.data) / len(self.data)) ** 0.5

    def _process_one_sample(self, sample: np.ndarray):
        return np.std(sample)

    def get_feature(self):
        self._process_dataset()
        data_dict = {"x": len(self.data), "y": self.data}
        df = pd.DataFrame(data_dict)
        feature = FeatureData(self.feature_name, df, self.min, self.max, self.mean, self.std)
        return feature

