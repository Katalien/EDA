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
    def _read_pdf(self):
        config_processor = ConfigReader(self.config_path)
        self.images_path = config_processor.get_images_path()
        self.output_path = config_processor.get_output_path()
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        features_config = config_processor.get_features_config()
        return features_config

    def run(self):
        features_config = self._read_pdf()
        features2analyse = buildFeatures(features_config)
        print(features2analyse)
        plots = []
        feature_list = []
        for analyzer, visual_methods in features2analyse.items():
            feature_analyzer = ClassNamesDict.AnalysersClassNamesDict[analyzer](self.images_path)
            features = feature_analyzer.get_feature()
            feature_list.append(features)
            if type(features) is not List[FeatureData]:
                features = [features]
            for visual_method in visual_methods:
                visualizer = ClassNamesDict.VisualizersClassNamesDict[visual_method]()
                plots.append(visualizer.visualize(features))

        pdfWriter = PdfWriter()
        pdfWriter.create_pdf_report(feature_list, plots, self.output_path + "report.pdf")