import os
from ConfigReader import ConfigReader
import os
from typing import List
from ConfigReader import ConfigReader
from utils import buildFeatures, ClassNamesDict
from PdfWriter import PdfWriter
from FeatureAnalysis import FeatureData


class Manager:
    def __init__(self, config_path: str = "./config.yaml"):
        self.config_path = config_path
        self.general_features_values = {}
        self.general_feature_plots = []
        self.labeled_features_values = {}
        self.labeled_feature_plots = []
        self.predicted_features_values = {}
        self.predicted_feature_plots = []

    def _read_config(self):
        config_processor = ConfigReader(self.config_path)
        self.images_path = config_processor.get_images_path()
        self.labels_path = config_processor.get_labels_path()
        self.output_path = config_processor.get_output_path()

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        self.general_features = config_processor.get_general_features()
        self.labeled_features = config_processor.get_labeled_features()
        self.predicted_features = config_processor.get_predicted_features()

    def process_features(self, feature_dict, path):
        plots = []
        feature_list = []
        for analyzer, visual_methods in feature_dict.items():
            feature_analyzer = ClassNamesDict.AnalysersClassNamesDict[analyzer](path)
            features = feature_analyzer.get_feature()
            if isinstance(features, List):
                for feature in features:
                    feature_list.append(feature)
            else:
                feature_list.append(features)
                features = [features]

            for visual_method in visual_methods:
                visualizer = ClassNamesDict.VisualizersClassNamesDict[visual_method]()
                plots.append(visualizer.visualize(features))
        return feature_list, plots


    def run(self):
        self._read_config()
        if self.general_features is not None:
            self.general_features_values, self.general_feature_plots = self.process_features(self.general_features, self.images_path)
        if self.labeled_features is not None:
            self.labeled_features_values, self.labeled_feature_plots = self.process_features(self.labeled_features, self.labels_path)

        feature_list = self.general_features_values
        feature_list.extend(self.labeled_features_values)

        plots = self.general_feature_plots
        plots.extend(self.labeled_feature_plots)
        pdfWriter = PdfWriter()
        pdfWriter.create_pdf_report(feature_list, plots, self.output_path + "report.pdf")


