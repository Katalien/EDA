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

class ClassAtributes:
    def __init__(self):
        self.square = None
        self.perimeter = None
        self.diameter = None
        self.bb_aspect_ratio = None


class ClassesAtributesAnalysis(FeatureAnalysis):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.dataset_info = dataset_info
        self.feature_name = "Classes atributes"
        self.classes_atributes_dict = {}

    def _fill_classes_atributes_dict(self):
        for class_name in self.dataset_info.dataset_classes.values():
            self.classes_atributes_dict[class_name] = ClassAtributes()

    def _process_dataset(self):
        file_dirs_dict = self.dataset_info.masks_path
        for i, (class_name, paths) in enumerate(file_dirs_dict.items()):
            for filepath in paths:
                image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
                self._process_one_sample(image, class_name)

    def _process_one_sample(self, sample: np.ndarray, class_name: str):
        contours, _ = cv2.findContours(sample, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        num_segments = len(contours)

        if str(class_name) in list(self.classes_frequency.keys()):
            self.classes_frequency[class_name] += num_segments
        else:
            self.classes_frequency[class_name] = num_segments

