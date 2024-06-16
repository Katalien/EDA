import os
import json
import pandas as pd
from FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.FeatureData import FeatureData


class ClassesFrequencyAnalysis(FeatureAnalysis):
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
        print(data_dict)
        feature = FeatureData(self.feature_name, data_dict)
        return feature



