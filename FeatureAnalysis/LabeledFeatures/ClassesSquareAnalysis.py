import os
import json
import cv2
import numpy as np
from FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.FeatureData import FeatureData
from DatasetProcessor import DatasetInfo
from .LabeledFeatures import LabeledFeatures

# общее количество всех классов в датасете
class ClassesSquareAnalysis(LabeledFeatures):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.feature_name = "Classes square"

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





