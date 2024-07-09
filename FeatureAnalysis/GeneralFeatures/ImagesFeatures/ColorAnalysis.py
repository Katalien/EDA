from FeatureAnalysis.FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.ClassFeatureData import ClassFeatureData
from DatasetProcessor import DatasetInfo
from .ImagesFeatures import ImagesFeatures
from ... import FeatureSummary
import matplotlib.pyplot as plt
from .ChanelAnalysis import ChanelAnalysis
import numpy as np
import cv2


class ColorAnalysis(ImagesFeatures):

    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.dataset_info = dataset_info
        self.feature_name = "Colors"
        # self.pixel_frequency_per_channel = np.zeros(256, dtype=np.int64)
        self.colors_feature_list = []
        self.colors = ["r", "g", "b"]
        self.all_hist_b = []
        self.all_hist_g = []
        self.all_hist_r = []
        self.data = {}

    def calculate_histogram(self, image):
        hist_b = cv2.calcHist([image], [0], None, [256], [0, 256])
        hist_g = cv2.calcHist([image], [1], None, [256], [0, 256])
        hist_r = cv2.calcHist([image], [2], None, [256], [0, 256])
        return hist_b, hist_g, hist_r

    def normalize_histogram(self, hist):
        return hist / hist.sum()

    def _process_dataset(self):
        file_dirs = self.dataset_info.images_path
        for i, filepath in enumerate(file_dirs):
            image = cv2.imread(filepath)
            hist_b, hist_g, hist_r = self.calculate_histogram(image)

            self.all_hist_b.append(self.normalize_histogram(hist_b))
            self.all_hist_g.append(self.normalize_histogram(hist_g))
            self.all_hist_r.append(self.normalize_histogram(hist_r))

        self.all_hist_b = np.array(self.all_hist_b)
        self.all_hist_g = np.array(self.all_hist_g)
        self.all_hist_r = np.array(self.all_hist_r)

        # Compute the average histograms
        avg_hist_b = np.mean(self.all_hist_b, axis=0)
        avg_hist_g = np.mean(self.all_hist_g, axis=0)
        avg_hist_r = np.mean(self.all_hist_r, axis=0)

        self.data["r"] = avg_hist_r
        self.data["g"] = avg_hist_g
        self.data["b"] = avg_hist_b




    def _process_one_sample(self, sample: np.ndarray):
        pass

    def get_feature(self) -> FeatureSummary:
        self._process_dataset()
        features = []
        for color in self.colors:
            chanel_hist = self.data[color]
            data_dict = {"x": range(256), "y": chanel_hist}

            feature = ClassFeatureData(self.feature_name,
                                       data_dict,
                                       class_name=str(color))
            features.append(feature)
        self.summary = FeatureSummary.FeatureSummary(self.feature_name, features)
        self.summary.set_description("RGB channels' analysis of images in dataset")
        return self.summary
