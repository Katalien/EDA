import os
import json
import pandas as pd
from FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.FeatureData import FeatureData


class InstancePerImageAnalysis(FeatureAnalysis):
    def __init__(self, labels_path: str):
        super().__init__(labels_path)
        self.labels_path = labels_path
        self.feature_name = "Classes frequency"
        self.classes_frequency = {}

    def _process_dataset(self):
        for json_file in os.listdir(self.labels_path):
            self._process_one_sample(json_file)


    def _process_one_sample(self, sample: str ):
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



