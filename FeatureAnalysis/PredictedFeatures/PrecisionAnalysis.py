import os
import json
import cv2
import numpy as np
import pandas as pd
from FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.FeatureData import FeatureData


class PrecisionAnalysis(FeatureAnalysis):
    def __init__(self, gt_masks_path: str, predictions_path: str):
        super().__init__(gt_masks_path)
        self.gt_masks_path = gt_masks_path
        self.prediction_masks_path = predictions_path
        self.feature_name = "Precision"
        self.classes_frequency = {}
        self.color_type_dict = {}
        self.data = []

    def _fill_data_info(self):
        for filename in os.listdir(self.gt_masks_path):
            if filename.endswith('.json'):
                file_path = os.path.join(self.gt_masks_path, filename)
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    for item in data:
                        color = tuple(item['color'])  # Преобразование списка цвета в кортеж
                        type_ = item['type']
                        self.color_type_dict[color] = type_

    def _process_dataset(self):
        for mask_filename in os.listdir(self.gt_masks_path):
            pred_mask_path = os.path.join(self.prediction_masks_path, mask_filename)
            gt_mask_path = os.path.join(self.gt_masks_path, mask_filename)
            gt_mask = cv2.imread(gt_mask_path)
            pred_mask = cv2.imread(pred_mask_path)
            self.data.append(self._process_one_sample(gt_mask, pred_mask))
        self.min = min(self.data)
        self.max = max(self.data)
        self.mean = sum(self.data) / len(self.data)
        self.std = (sum((x - self.mean) ** 2 for x in self.data) / len(self.data)) ** 0.5


    def _process_one_sample(self, sample: np.ndarray, pred: np.ndarray):
        # Precision as TP / (TP + FP)
        tp_mask = cv2.bitwise_and(sample, pred)
        fp_mask = cv2.bitwise_and(cv2.bitwise_not(sample), pred)
        tp = np.sum(tp_mask == 255)
        fp = np.sum(fp_mask == 255)
        return tp / (tp + fp)



    def get_feature(self):
        self._process_dataset()
        data_dict = {"x": len(self.data), "y": self.data}
        print(data_dict)
        df = pd.DataFrame(data_dict)
        feature = FeatureData(self.feature_name, df, self.min, self.max, self.mean, self.std)
        return feature



