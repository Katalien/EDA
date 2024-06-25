import os
import json
import cv2
import numpy as np
import pandas as pd
from FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.FeatureData import FeatureData
from DatasetProcessor import FileIterator
from utils import Classes

# общее количество всех классов в датасете
class ClassesFrequencyAnalysis(FeatureAnalysis):
    def __init__(self, labels_path: str):
        super().__init__(labels_path)
        self.labels_path = labels_path
        self.feature_name = "Classes frequency"
        self.classes_frequency = {}

    def _process_dataset(self):
        image_files, file_dirs = FileIterator.get_images_from_lowest_level_folders(self.path)
        for i, dir_path in enumerate(file_dirs):
            for image_name in os.listdir(dir_path):
                if len(image_name.split("_")) != 1:  # skip original image
                    class_name = image_name.split("_")[1].split(".")[0]
                    if class_name not in list(Classes.DatasetClasses.keys()):
                        print(f"Unkwown class in {dir_path}, no class {class_name}")
                        continue
                    filepath = os.path.join(os.path.normpath(dir_path), image_name)
                    filepath = filepath.replace("\\", "/")
                    image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
                    self._process_one_sample(image, class_name)
    def _process_one_sample(self, sample: np.ndarray,  class_name:str):
        contours, _ = cv2.findContours(sample, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        num_segments = len(contours)
        dict_class_name = Classes.DatasetClasses[class_name]
        if str(dict_class_name) in list(self.classes_frequency.keys()):
            self.classes_frequency[dict_class_name] += num_segments
        else:
            self.classes_frequency[dict_class_name] = num_segments

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



