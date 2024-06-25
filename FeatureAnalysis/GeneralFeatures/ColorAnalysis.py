import os
from FeatureAnalysis.FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.FeatureData import FeatureData
from DatasetProcessor import FileIterator
import numpy as np
import pandas as pd
import cv2


class ChanelAnalysis(FeatureAnalysis):
    def __init__(self, path: str, color: str):
        super().__init__(path)
        self.color = color
        self.feature_name = color.capitalize()
        self.pixel_frequency_per_channel = np.zeros(256, dtype=np.int64)
        self.palette = {color: color}
        if color not in ["r", "g", "b"]:
            raise ValueError("Color must be 'r', 'g', or 'b'.")

    def _process_dataset(self):
        image_files, file_dirs = FileIterator.get_images_from_lowest_level_folders(self.path)
        for i, dir_path in enumerate(file_dirs):
            for image_name in os.listdir(dir_path):
                if len(image_name.split("_")) == 1:  # get original image
                    filepath = os.path.join(os.path.normpath(dir_path), image_name)
                    filepath = filepath.replace("\\", "/")
                    image = cv2.imread(filepath)
                    if image is not None:
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

    def __init__(self, path: str):
        super().__init__(path)
        self.feature_name = "Colors"
        self.pixel_frequency_per_channel = np.zeros(256, dtype=np.int64)
        self.colors_feature_list = []


    def _process_dataset(self):
        colors = ["r", "g", "b"]
        for color in colors:
            chanel_analyzer = ChanelAnalysis(self.path, color)
            self.colors_feature_list.append(chanel_analyzer.get_feature())

    def _process_one_sample(self, sample: np.ndarray):
        pass

    def get_feature(self):
        self._process_dataset()
        return self.colors_feature_list

