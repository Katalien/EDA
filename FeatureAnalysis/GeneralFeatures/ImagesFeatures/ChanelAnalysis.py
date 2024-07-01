from FeatureAnalysis.ClassFeatureData import ClassFeatureData
from DatasetProcessor import DatasetInfo
from .ImagesFeatures import ImagesFeatures
import numpy as np
import cv2


class ChanelAnalysis(ImagesFeatures):
    def __init__(self, dataset_info: DatasetInfo, color: str):
        super().__init__(dataset_info)
        self.color = color
        self.feature_name = color.capitalize()
        self.pixel_frequency_per_channel = np.zeros(256, dtype=np.int64)
        self.palette = {color: color}
        if color not in ["r", "g", "b"]:
            raise ValueError("Color must be 'r', 'g', or 'b'.")

    def _process_dataset(self):
        file_dirs = self.dataset_info.images_path
        for i, filepath in enumerate(file_dirs):
            image = cv2.imread(filepath)
            self._process_one_sample(image)

    def _process_one_sample(self, sample: np.ndarray):
        color_idx = {"r": 2, "g": 1, "b": 0}
        channel_idx = color_idx[self.color]
        self.pixel_frequency_per_channel += np.histogram(sample[:, :, channel_idx], bins=256)[0]

    def get_feature(self):
        self._process_dataset()
        data_dict = {"x": list(range(256)), "y": list(self.pixel_frequency_per_channel)}
        min_value = min(data_dict["y"])
        max_value = max(data_dict["y"])
        mean_value = float(np.mean(data_dict["y"]))
        std_value = float(np.std(data_dict["y"]))

        feature_data = ClassFeatureData(
            feature_name=self.feature_name,
            data=data_dict,
            _min=min_value,
            _max=max_value,
            _mean=mean_value,
            _std=std_value
        )

        return feature_data
