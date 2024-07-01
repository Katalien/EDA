from FeatureAnalysis.FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.ClassFeatureData import ClassFeatureData
from DatasetProcessor import DatasetInfo
from .ImagesFeatures import ImagesFeatures
from ... import FeatureSummary
from .ChanelAnalysis import ChanelAnalysis
import numpy as np
import cv2


class ColorAnalysis(ImagesFeatures):

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

    def get_feature(self) -> FeatureSummary:
        self._process_dataset()
        self.summary = FeatureSummary.FeatureSummary(self.feature_name, self.colors_feature_list)
        self.summary.set_description("RGB channels' analysis of images in dataset")
        return self.summary
