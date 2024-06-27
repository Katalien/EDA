import os
import json
import cv2
import numpy as np
import pandas as pd
from FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.FeatureData import FeatureData
from DatasetProcessor import FileIterator, DatasetInfo
from DatasetProcessor import DatasetInfo
from utils import Classes

# общее количество всех классов в датасете
class ClassesSquareAnalysis(FeatureAnalysis):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.dataset_info = dataset_info
        self.feature_name = "Classes square"
        self.classes_frequency = {}

    def _process_dataset(self):
        file_dirs_dict = self.dataset_info.masks_path
        for i, (class_name, paths) in enumerate(file_dirs_dict.items()):
            for filepath in paths:
                image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
                self._process_one_sample(image, class_name)
    def _process_one_sample(self, sample: np.ndarray,  class_name:str):
        contours, _ = cv2.findContours(sample, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        num_segments = len(contours)

        if str(class_name) in list(self.classes_frequency.keys()):
            self.classes_frequency[class_name] += num_segments
        else:
            self.classes_frequency[class_name] = num_segments

    def _process_dataset_json(self):
        for json_file in os.listdir(self.labels_path):
            self._process_one_sample(json_file)

    def _process_one_sample_json(self, sample: str ):
        filepath = os.path.join(self.labels_path, sample)
        with open(filepath, "r") as file:
            json_data = json.load(file)
            for data_line in json_data:
                defect_type = data_line["type"]
                if str(defect_type) in self.classes_frequency:
                    self.classes_frequency[defect_type] += 1
                else:
                    self.classes_frequency[defect_type] = 1

    def get_feature(self):
        self._process_dataset()
        data_dict = {"x": list(self.classes_frequency.keys()), "y": list(self.classes_frequency.values())}
        for key, val in self.classes_frequency.items():
            print(key, val)
        feature = FeatureData(self.feature_name, data_dict)
        return feature



