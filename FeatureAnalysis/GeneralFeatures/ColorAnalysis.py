from FeatureAnalysis.FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.FeatureData import FeatureData
from DatasetProcessor import DatasetInfo
import numpy as np
import cv2


class ChanelAnalysis(FeatureAnalysis):
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

        # print(cv2.calcHist(sample[:, :, channel_idx], [channel_idx], None, [256], [0, 256]))
        # self.pixel_frequency_per_channel.append(cv2.calcHist(sample[:, :, channel_idx], [channel_idx], None, [256], [0, 256]))

    def get_feature(self):
        self._process_dataset()
        data_dict = {"x": list(range(256)), "y": list(self.pixel_frequency_per_channel)}
        min_value = min(data_dict["y"])
        max_value = max(data_dict["y"])
        mean_value = float(np.mean(data_dict["y"]))
        std_value = float(np.std(data_dict["y"]))

        feature_data = FeatureData(
            feature_name=self.feature_name,
            data=data_dict,
            min=min_value,
            max=max_value,
            mean=mean_value,
            std=std_value
        )

        return feature_data


class ColorAnalysis(FeatureAnalysis):

    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.dataset_info = dataset_info
        self.feature_name = "Colors"
        self.pixel_frequency_per_channel = np.zeros(256, dtype=np.int64)
        self.colors_feature_list = []


    def _process_dataset(self):
        colors = ["r", "g", "b"]
        for color in colors:
            chanel_analyzer = ChanelAnalysis(self.dataset_info, color)
            self.colors_feature_list.append(chanel_analyzer.get_feature())

    def _process_one_sample(self, sample: np.ndarray):
        pass

    def get_feature(self):
        self._process_dataset()
        return self.colors_feature_list