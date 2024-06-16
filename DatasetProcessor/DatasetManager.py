import os
from ConfigReader import ConfigReader
import os
from typing import List
from ConfigReader import ConfigReader
from utils import buildFeatures, ClassNamesDict
from PdfWriter import PdfWriter
from .SampleSummary import SampleSummary
from FeatureAnalysis import FeatureData


def get_package_files(root_dir):
    file_package_map = {}
    for root, dirs, files in os.walk(root_dir):
        package_name = os.path.basename(root)
        if package_name == "":
            continue
        for file in files:
            if file.endswith(".py"):
                file_name = os.path.splitext(file)[0].replace("Analysis", "")
                file_package_map[file_name] = package_name
    return file_package_map


images_features_path = {
    "GeneralFeatures": "images",
    "LabeledFeatures": "labels",
    "PredictedFeatures": ["labels", "predictions"]
}

class Manager:
    def __init__(self, config_path: str = "./config.yaml"):
        self.config_path = config_path
        self.dir_tags = {"train": False, "val": False, "test": False}
        self.summary = {}
        self.analysis_files = get_package_files("./FeatureAnalysis/")

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

    def _check_folder(self, analyzer, filepath):
        analyzer_package = self.analysis_files.get(analyzer, None)
        if analyzer_package is  None:
            # print(f"No such analyzer {analyzer}")
            return
        target_folder = images_features_path[analyzer_package]
        # print(target_folder)
        cur_dirs = os.listdir(filepath)
        if target_folder not in cur_dirs:
            # print(f"Error. No folder to analyse. {analyzer} needs {target_folder}")
            return
        else:
            # print(f"FINE! {analyzer} HAVE {target_folder}")
            return os.path.join(filepath, target_folder)


    def process(self):
        # read config
        config_processor = ConfigReader(self.config_path)
        self.dataset_path = config_processor.get_dataset_path()
        self.output_path = config_processor.get_output_path()
        self.features = config_processor.get_features()
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)


        current_dataset_tags = os.listdir(self.dataset_path)
        for dir in os.listdir(self.dataset_path):
            print(dir)
            if dir in list(self.dir_tags):
                folder_path = os.path.join(self.dataset_path, dir)
                plots, feature_list = [], []
                for analyzer, visual_methods in self.features.items():
                    target_folder = self._check_folder(analyzer, folder_path)
                    if target_folder is None:
                        continue

                    print(analyzer)
                    feature_analyzer = ClassNamesDict.AnalysersClassNamesDict[analyzer](target_folder)
                    features = feature_analyzer.get_feature()
                    if features is None:
                        continue
                    if isinstance(features, List):
                        for feature in features:
                            feature_list.append(feature)
                    else:
                        feature_list.append(features)
                        features = [features]

                    for visual_method in visual_methods:
                        visualizer = ClassNamesDict.VisualizersClassNamesDict[visual_method]()
                        plots.append(visualizer.visualize(features))

                self.summary[dir] = SampleSummary(feature_list, plots, dir)

        for key, val in self.summary.items():
            print(key)
            print(val)










