import os
import json
from FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.FeatureData import FeatureData
from .LabeledFeatures import LabeledFeatures
from DatasetProcessor import DatasetInfo
import cv2
import numpy as np


class InstancePerImageAnalysis(LabeledFeatures):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.feature_name = "Instance pre image"


#TODO находит лишние контуры как исправить
    def _process_one_sample(self, sample: np.ndarray, class_name: str):
        kernel = np.ones((22, 22), np.uint8)
        sample = cv2.morphologyEx(sample, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(sample, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        num_segments = len(contours)

        if class_name not in self.classes_frequency:
            self.classes_frequency[class_name] = [num_segments]
        else:
            self.classes_frequency[class_name].append(num_segments)



    def _process_dataset_json(self):
        for json_file in os.listdir(self.labels_path):
            self._process_one_sample(json_file)


    def _process_one_sample_json(self, sample: str ):
        filepath = os.path.join(self.labels_path, sample)
        classes_per_image = {}
        with open(filepath, "r") as file:
            json_data = json.load(file)
            for data_line in json_data:
                defect_type = data_line["type"]
                if str(defect_type) in classes_per_image:
                    classes_per_image[defect_type] += 1
                else:
                    classes_per_image[defect_type] = 1
        for key, vals in classes_per_image.items():
            if key not in self.classes_frequency:
                self.classes_frequency[key] = [vals]
            else:
                self.classes_frequency[key].append(vals)

    def _fill_zeroes(self):
        max_len = -1
        for val in self.classes_frequency.values():
            if len(val) > max_len:
                max_len = len(val)
        for key, val in self.classes_frequency.items():
            if len(val) < max_len:
                val.extend([0] * (max_len - len(val)))


    def get_feature(self):
        self._process_dataset()
        self._fill_zeroes()
        features = []
        for key, val in self.classes_frequency.items():
            data_dict = {"x": len(list(val)), "y": list(val)}
            feature = FeatureData(f"Instance of {key} per Image.", data_dict)
            features.append(feature)
        return features



