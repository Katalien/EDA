from FeatureAnalysis.FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.FeatureData import FeatureData
import numpy as np
import cv2
import os
import pandas as pd
from DatasetProcessor import FileIterator

class AspectRatioAnalysis(FeatureAnalysis):
    def __init__(self, path: str):
        super().__init__(path)
        self.path = path
        self.feature_name = "Aspect Ratio"
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


    # def _process_dataset(self):
    #     for file in os.listdir(self.path):
    #         image = cv2.imread(os.path.join(self.path, file))
    #         self.data.append(self._process_one_sample(image))
    #     self.min = min(self.data)
    #     self.max = max(self.data)
    #     self.mean = sum(self.data) / len(self.data)
    #     self.std = (sum((x - self.mean) ** 2 for x in self.data) / len(self.data)) ** 0.5

    def _process_one_sample(self, sample: np.ndarray):
        height, width = sample.shape[:2]
        return width / height

    def get_feature(self):
        if os.listdir(self.path) == []:
            print("empty")
            return
        self._process_dataset()
        data_dict = {"x": len(self.data), "y": self.data}
        df = pd.DataFrame(data_dict)
        feature = FeatureData(self.feature_name, df, self.min, self.max, self.mean, self.std)
        return feature
