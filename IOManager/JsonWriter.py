import json
import numpy as np
from FeatureAnalysis import FeatureSummary
from DatasetProcessor import DatasetInfo

class JsonWriter:
    def __init__(self, feature_summaries_list: list[FeatureSummary], dataset_info: DatasetInfo, save_filepath: str = "./"):
        self.feature_summaries_list: list = feature_summaries_list
        self.dataset_info = dataset_info
        self.save_filepath: str = save_filepath

    def __save_dataset_info(self):
        dataset_info_dict = {
            "dataset_path": self.dataset_info.dataset_path,
            "dataset_classes": self.dataset_info.dataset_classes,
            "images_count": self.dataset_info.images_count,
            "masks_count": self.dataset_info.masks_count,
            "equal_image_sizes": self.dataset_info.equal_image_sizes,
            "equal_mask_sizes": self.dataset_info.equal_mask_sizes
        }
        data_to_save = {"Dataset Info": dataset_info_dict}
        return data_to_save


    def save_feature_summary_to_json(self):
        data_to_save = self.__save_dataset_info()
        all_feature_summaries_dicts = []
        for feature_summary in self.feature_summaries_list:
            if feature_summary.is_img_feature:
                continue
            summary_dict = {
                "feature_name": feature_summary.feature_name,
                "feature_tag": feature_summary.feature_tag,
                "features_list": [
                    {
                        "feature_name": feature.feature_name,
                        "class_name": feature.class_name,
                        "data": JsonWriter.__process_data_dict(feature.data),
                        "min": JsonWriter.__convert_to_serializable(feature.min),
                        "max": JsonWriter.__convert_to_serializable(feature.max),
                        "mean": JsonWriter.__convert_to_serializable(feature.mean),
                        "std": JsonWriter.__convert_to_serializable(feature.std),
                        "is_img": feature.is_img
                    }
                    for feature in feature_summary.features_list
                ],
                "description": feature_summary.description,
                "visual_methods_name": feature_summary.visual_methods_name,
                "visual_settings": str(feature_summary.visual_settings)
            }
            all_feature_summaries_dicts.append(summary_dict)
        data_to_save["Features Info"] = all_feature_summaries_dicts

        with open(self.save_filepath, 'a') as f:
            json.dump(data_to_save, f, indent=4)

    @staticmethod
    def __convert_to_serializable(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            if len(obj.shape) == 2:
                obj = obj.reshape(obj.shape[0])
            return obj.tolist()
        elif isinstance(obj, range):
            return list(obj)
        else:
            return obj

    @staticmethod
    def __process_data_dict(data_dict):
        if not isinstance(data_dict, dict):
            return None
        return {
            "x": JsonWriter.__convert_to_serializable(data_dict["x"]),
            "y": JsonWriter.__convert_to_serializable(data_dict['y']),
        }