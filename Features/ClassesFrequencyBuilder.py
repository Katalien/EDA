import cv2
import numpy as np
from FeatureSummaryData import FeatureSummary
from FeatureSummaryData.ClassFeatureData import ClassFeatureData
from DatasetProcessor import DatasetInfo
import utils.utils as ut


class ClassesFrequencyBuilder:
    def __init__(self, dataset_info: DatasetInfo):
        self.dataset_info = dataset_info
        self.feature_name = "Classes frequency"
        self.data = {}
        self.summary: FeatureSummary = None

    def __process_dataset(self):
        sample_paths_items = self.dataset_info.get_samples_path_info()

        for sample_path_item in sample_paths_items:
            masks_path = sample_path_item.get_mask_path_dict()
            for class_name, filepath in masks_path.items():
                if filepath.split(".")[-1] == "psd":
                    image = ut.get_np_from_psd(filepath)
                else:
                    image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
                self.__process_one_sample(image, class_name)

    def __process_one_sample(self, sample: np.ndarray,  class_name: str):
        contours, _ = cv2.findContours(sample, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if str(class_name) in list(self.data.keys()):
            self.data[class_name] += len(contours)
        else:
            self.data[class_name] = len(contours)

    def __get_feature_info(self) -> FeatureSummary:
        self.__process_dataset()
        features = []
        for key, val in self.data.items():
            cur_class_freq = {"x": key, "y": val}
            cur_feature = ClassFeatureData(self.feature_name,
                                           cur_class_freq,
                                           class_name=key)
            features.append(cur_feature)
        self.summary = FeatureSummary.FeatureSummary(self.feature_name, features, feature_tag="Labels")
        return self.summary

    def get_feature(self) -> FeatureSummary:
        self.__get_feature_info()
        info = "General amount of classes in dataset: "
        for class_name, amount in self.data.items():
            info += f"\n {class_name} - {amount}; "
        self.summary.set_description(info)
        return self.summary



