import os
import json
import cv2
import numpy as np
import pandas as pd
from FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.FeatureData import FeatureData
from DatasetProcessor import FileIterator, DatasetInfo
from DatasetProcessor import DatasetInfo
from typing import Dict, List
from utils import Classes



class ClassesBbAspectRatioAnalysis(FeatureAnalysis):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.dataset_info = dataset_info
        self.feature_name = "Classes bb ratio"
        self.classes_bb_ratio_dict: Dict[str, List] = {}
        self.featuresData = []

    def _process_dataset(self):
        file_dirs_dict = self.dataset_info.masks_path
        for i, (class_name, paths) in enumerate(file_dirs_dict.items()):
            for filepath in paths:
                image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
                self._process_one_sample(image, class_name)
        for class_name, data in self.classes_bb_ratio_dict.items():
            _min = min(data)
            _max = max(data)
            _mean = sum(data) / len(data)
            _std = (sum((x - _mean) ** 2 for x in data) / len(data)) ** 0.5
            _data_dict = {"x": len(data), "y": data}
            _feature_name = f"{self.feature_name} {class_name}"
            feature = FeatureData(_feature_name, _data_dict, _min, _max, _mean, _std)
            self.featuresData.append(feature)



    def _process_one_sample(self, sample: np.ndarray,  class_name:str):
        contours, _ = cv2.findContours(sample, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h
            if str(class_name) not in list(self.classes_bb_ratio_dict.keys()):
                self.classes_bb_ratio_dict[class_name] = [aspect_ratio]
            else:
                self.classes_bb_ratio_dict[class_name].append(aspect_ratio)

    def get_feature(self):
        self._process_dataset()

        return self.featuresData

