from FeatureAnalysis.ClassFeatureData import ClassFeatureData
from DatasetProcessor import DatasetInfo
from FeatureAnalysis import FeatureSummary
from Visualizer.VisualizeSetiings import VisualizeSettings
import numpy as np
import cv2
import utils.utils as ut


class ColorHistogramBuilder:
    def __init__(self, dataset_info: DatasetInfo):
        self.dataset_info = dataset_info
        self.dataset_info = dataset_info
        self.feature_name = "Colors"
        self.colors_feature_list = []
        self.colors = ["r", "g", "b"]
        self.all_hist_b = []
        self.all_hist_g = []
        self.all_hist_r = []
        self.data = {}
        self.summary: FeatureSummary = None

    @staticmethod
    def __calculate_histogram(image):
        hist_b = cv2.calcHist([image], [0], None, [256], [0, 256])
        hist_g = cv2.calcHist([image], [1], None, [256], [0, 256])
        hist_r = cv2.calcHist([image], [2], None, [256], [0, 256])
        return hist_b, hist_g, hist_r
    @staticmethod
    def __normalize_histogram(hist):
        return hist / hist.sum()

    def __process_dataset(self):
        file_dirs = self.dataset_info.get_images_paths()
        for i, filepath in enumerate(file_dirs):
            if filepath.split(".")[-1] == "psd":
                image = ut.get_np_from_psd(filepath)
            else:
                image = cv2.imread(filepath)
            hist_b, hist_g, hist_r = ColorHistogramBuilder.__calculate_histogram(image)

            self.all_hist_b.append(ColorHistogramBuilder.__normalize_histogram(hist_b))
            self.all_hist_g.append(ColorHistogramBuilder.__normalize_histogram(hist_g))
            self.all_hist_r.append(ColorHistogramBuilder.__normalize_histogram(hist_r))

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

    def get_feature(self) -> FeatureSummary:
        self.__process_dataset()
        features = []
        for color in self.colors:
            chanel_hist = self.data[color]
            data_dict = {"x": range(256), "y": chanel_hist}
            feature = ClassFeatureData(self.feature_name, data_dict, class_name=str(color))
            features.append(feature)

        vis_settings = VisualizeSettings(title="Channel distributions",
                                         subplots=True,
                                         colors=["red", "green", "blue"],
                                         subtitles=["Red", "Green", "Blue"],
                                         x_axes="Pixel Value",
                                         y_axes="Frequency",
                                         grid=True)
        self.summary = FeatureSummary.FeatureSummary(self.feature_name,
                                                     features,
                                                     visual_settings=vis_settings,
                                                     feature_tag="General")
        self.summary.set_description("RGB channels' analysis of images in dataset. Values are normalized")
        return self.summary
