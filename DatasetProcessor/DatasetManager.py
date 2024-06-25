import os
from ConfigReader import ConfigReader
import os
from typing import List
from ConfigReader import ConfigReader
from utils import buildFeatures, ClassNamesDict
from PdfWriter import PdfWriter
from .FeatureSummary import FeatureSummary
from DatasetProcessor import DatasetInfo
from FeatureAnalysis import FeatureData

GeneralFeatures = ["AspectRatio", "Brightness", "Color", "Contrast"]
LabeledFeatures = ["ClassesFrequency", "InstancesPerImage", "LocationMap"]
PredictedFeatures = ["Precision", "Recall"]

class DatasetManager:
    def __init__(self, config_path: str = "./config.yaml"):
        self.config_path = config_path
        self.featureSummaries = []
        self.classes = None
        self.dataset_path = None
        self.output_path = None
        self.dataset_info = None
        self.dataset_classes = None

    def _read_config(self):
        config_processor = ConfigReader(self.config_path)
        self.dataset_path = config_processor.get_dataset_path()
        self.output_path = config_processor.get_output_path()
        self.dataset_info = DatasetInfo.DatasetInfo(self.dataset_path)
        self.features = config_processor.get_features()

    def _check_info_4_feature(self, feature_name):
        if feature_name in GeneralFeatures and self.dataset_info.images_path is None:
            return False
        if feature_name in LabeledFeatures and self.dataset_info.masks_path is None:
            return False
        if feature_name in PredictedFeatures and self.dataset_info.prediction_path is None:
            return False
        return True

    def _get_target_info(self, feature_name):
        if feature_name in GeneralFeatures:
            return self.dataset_info.images_path
        if feature_name in LabeledFeatures:
            return self.dataset_info.masks_path
        if feature_name in PredictedFeatures:
            # sort
            return [self.dataset_info.masks_path, self.dataset_info.prediction_path]

    def run(self):
        self._read_config()
        for feature_name, visual_methods in self.features.items():
            plots = []
            if not self._check_info_4_feature(feature_name):
                print(f"No info for this feature: {feature_name}")
                continue

            feature_analyzer = ClassNamesDict.AnalysersClassNamesDict[feature_name](self.dataset_info)
            features = feature_analyzer.get_feature()
            featureSummary = FeatureSummary(feature_name, features, visual_methods)
            for visual_method in visual_methods:
                visualizer = ClassNamesDict.VisualizersClassNamesDict[visual_method]()
                plots.append(visualizer.visualize(featureSummary))
            featureSummary.set_plots(plots)
            self.featureSummaries.append(featureSummary)

        print(type(self.featureSummaries))
        pdfWriter = PdfWriter(self.featureSummaries, self.dataset_info, self.output_path + "report.pdf")
        pdfWriter.write()
