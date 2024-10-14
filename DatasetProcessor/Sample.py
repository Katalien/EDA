from typing import Dict, List
from .SamplePathInfo import SamplePathInfo
import cv2
import utils.utils as ut
from Features import Feature, BrightnessFeature, ContrastFeature, AspectRatioFeature, MaskedContrastFeature, \
    MaskedBrightnessFeature, MaskedGradientFeature, InstancePerImageFeature, ClassesAreaFeature, \
    ClassesBBAspectRatioFeature, ClassesDiameterFeature, Class2ImageRatioFeature

feature_class_dict = {
    "Brightness": BrightnessFeature.BrightnessFeature,
    "Contrast": ContrastFeature.ContrastFeature,
    "AspectRatio": AspectRatioFeature.AspectRatioFeature,
    "MaskedBrightness": MaskedBrightnessFeature.MaskedBrightnessFeature,
    "MaskedContrast": MaskedContrastFeature.MaskedContrastFeature,
    "MaskedGradient": MaskedGradientFeature.MaskedGradientFeature,
    "InstancesPerImage": InstancePerImageFeature.InstancePerImageFeature,
    "ClassesArea": ClassesAreaFeature.ClassesAreaFeature,
    "ClassesBbAspectRatio": ClassesBBAspectRatioFeature.ClassesBBAspectRatioFeature,
    "ClassesDiameter": ClassesDiameterFeature.ClassesDiameterFeature,
    "Class2ImageRatio":   Class2ImageRatioFeature.Class2ImageRatioFeature
}

class Sample:
    def __init__(self, sample_path_info: SamplePathInfo,  feature_list: List):
        self.sample_path_info: SamplePathInfo = sample_path_info
        self.mask_classes = []
        self.feature_values_dict: Dict = {}
        for feature in feature_list:
            self.feature_values_dict[feature] = None
        self.__fill_mask_classes()

    def __fill_mask_classes(self):
        self.mask_classes = ["General"]
        for class_name in self.sample_path_info.get_mask_path_dict().keys():
            self.mask_classes.append(class_name)

    def get_all_mask_classes(self):
        return self.mask_classes

    def fill_features_info(self):
        for feature in self.feature_values_dict.keys():
            try:
                if feature in feature_class_dict:
                    feature_class = feature_class_dict[feature]()
                    feature_value = feature_class.calculate(self)
                    self.feature_values_dict[feature] = feature_value
                else:
                    raise KeyError(f"No such feature available {feature}")
            except KeyError as e:
                print(f"Error {e}. Skipping feature {feature}")

    def get_feature_info(self, feature_name):
        pass

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

