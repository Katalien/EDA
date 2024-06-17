import os
import json
import cv2
import numpy as np
import pandas as pd
from FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.FeatureData import FeatureData


class LocationsMap(FeatureAnalysis):
    def __init__(self, labels_path: str):
        super().__init__(labels_path)
        self.path = labels_path
        self.feature_name = "Object location map"
        self.res_image = np.zeros(shape=(self._get_image_size()), dtype=np.uint8)

    def _process_dataset(self):
        sample_count = len(os.listdir(self.path))
        weigth = 1/sample_count
        for file in os.listdir(self.path):
            filepath = os.path.join(self.path, file)
            cur_im = cv2.imread(filepath)
            self.res_image = cv2.addWeighted(self.res_image, 1, cur_im, weigth, 0)


    def _get_image_size(self):
        for file in os.listdir(self.path):
            filepath = os.path.join(self.path, file)
            im = cv2.imread(filepath)
            return im.shape


    def _process_one_sample(self, sample: str ):
        pass
        # filepath = os.path.join(self.labels_path, sample)
        # with open(filepath, "r") as file:
        #     json_data = json.load(file)
        #     for data_line in json_data:
        #         defect_type = data_line["type"]
        #         if str(defect_type) in self.classes_frequency:
        #             self.classes_frequency[defect_type] += 1
        #         else:
        #             self.classes_frequency[defect_type] = 1

    def get_feature(self):
        self._process_dataset()
        feature = FeatureData(self.feature_name, self.res_image, is_img=True)
        return feature



