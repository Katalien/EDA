from typing import Dict, List
from .SamplePathInfo import SamplePathInfo
import cv2
import utils.utils as ut
from utils import FeatureMetadata


class Sample:
    def __init__(self, sample_path_info: SamplePathInfo,  feature_list: List):
        self.sample_path_info: SamplePathInfo = sample_path_info
        self.mask_classes = []
        self.feature_values_dict: Dict = {}
        self.__classes_contours: Dict = {}
        self.__fill_classes_contours()
        for feature in feature_list:
            self.feature_values_dict[feature] = None
        self.__fill_mask_classes()

    def __fill_mask_classes(self):
        self.mask_classes = ["General"]
        for class_name in self.sample_path_info.get_mask_path_dict().keys():
            self.mask_classes.append(class_name)

    def get_all_mask_classes(self):
        return self.mask_classes

    def __fill_classes_contours(self):
        for mask_class, mask_path in self.sample_path_info.get_mask_path_dict().items():
            if mask_class == "General":
                continue
            mask = self.load_mask(mask_class)
            contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
            self.__classes_contours[mask_class] = contours

    def get_contours(self):
        return self.__classes_contours

    def get_contours_by_class(self, class_name):
        return self.__classes_contours[class_name]

    def fill_features_info(self):
        for feature in self.feature_values_dict.keys():
            if feature in FeatureMetadata.FeatureClassDict:
                feature_class = FeatureMetadata.FeatureClassDict[feature]()
                feature_value = feature_class.calculate(self)
                self.feature_values_dict[feature] = feature_value

    def load_image(self):
        image_path = self.sample_path_info.get_image_path()
        if image_path.split(".")[-1] != "psd":
            return cv2.imread(image_path)
        else:
            return ut.get_np_from_psd(image_path)

    def load_mask(self, class_name):
        mask_path = self.sample_path_info.get_mask_path_by_tag(class_name)
        return cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

    def get_feature_val_by_feature_name(self, feature_name):
        return self.feature_values_dict[feature_name]

    def get_feature_values(self):
        return self.feature_values_dict

