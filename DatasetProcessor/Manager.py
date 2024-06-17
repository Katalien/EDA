import os
from ConfigReader import ConfigReader
import os
from typing import List
from ConfigReader import ConfigReader
from utils import buildFeatures, ClassNamesDict
from PdfWriter import PdfWriter
from .FeatureSummary import FeatureSummary
from FeatureAnalysis import FeatureData


class Manager:
    def __init__(self, config_path: str = "./config.yaml"):
        self.config_path = config_path
        self.featureSummaries = []
        self.classes = None


    def _read_config(self):
        config_processor = ConfigReader(self.config_path)
        self.images_path = config_processor.get_images_path()
        self.labels_path = config_processor.get_labels_path()
        self.masks_path = config_processor.get_masks_path()
        self.prediction_path = config_processor.get_prediction_path()
        self.features = config_processor.get_features()
        self.output_path = config_processor.get_output_path()

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def _check_dir4feature(self, feature_name):
        dirs2check = ClassNamesDict.FeatureFolderDict[feature_name]
        for dir2check in dirs2check:
            if dir2check == "labels" and self.labels_path is None:
                return False
            if dir2check == "predictions" and self.prediction_path is None:
                return False
        return True

    def _get_target_path(self, feature_name):
        target_folder = ClassNamesDict.FeatureFolderDict[feature_name]
        if "labels" in target_folder and "predictions" in target_folder:
            return [self.labels_path, self.prediction_path]
        if "masks" in target_folder and "predictions" in target_folder:
            return [self.masks_path, self.prediction_path]
        if "labels" in target_folder:
            return self.labels_path
        if "masks" in target_folder:
            return self.masks_path
        if "images" in target_folder:
            return self.images_path

    def _count_samples_with_ext(self, directory_path, extensions):
        count = 0
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensions):
                    count += 1
        return count

    def _get_dataset_sample_count(self):
        dataset_count_dict = {}
        if self.images_path is not None:
            extensions = [".jpg", ".tiff", ".png"]
            count = self._count_samples_with_ext(self.images_path, extensions)
            dataset_count_dict["images"] = count
        if self.labels_path is not None:
            extensions = [".txt", ".json"]
            count = self._count_samples_with_ext(self.images_path, extensions)
            dataset_count_dict["labels"] = count
        if self.prediction_path is not None:
            extensions = [".json", ".jpg", ".png"]
            count = self._count_samples_with_ext(self.images_path, extensions)
            dataset_count_dict["predictions"] = count
        return dataset_count_dict



    def run(self):
        self._read_config()
        dataset_count_dict = self._get_dataset_sample_count()
        plots, feature_list = [], []
        for feature_name, visual_methods in self.features.items():
            if not self._check_dir4feature(feature_name):
                print(f"No folder for this feature: {feature_name}. Necessary to have {ClassNamesDict.FeatureFolderDict[feature_name]} dir")
                continue
            target_folder = self._get_target_path(feature_name)
            if isinstance(target_folder, List):
                label_folder = target_folder[0]
                pred_folder = target_folder[1]
                feature_analyzer = ClassNamesDict.AnalysersClassNamesDict[feature_name](label_folder, pred_folder)
            else:
                feature_analyzer = ClassNamesDict.AnalysersClassNamesDict[feature_name](target_folder)
            features = feature_analyzer.get_feature()
            featureSummary = FeatureSummary(feature_name, features, visual_methods)
            for visual_method in visual_methods:
                visualizer = ClassNamesDict.VisualizersClassNamesDict[visual_method]()
                plots.append(visualizer.visualize(features))
            featureSummary.set_plots(plots)
            self.featureSummaries.append(featureSummary)
        for feature_sum in self.featureSummaries:
            for plot in feature_sum.plots:
                plot.show()


            # if features is None:
            #     continue
            #
            # if isinstance(features, List):
            #     for feature in features:
            #         feature_list.append(feature)
            # else:
            #     if features.is_img:
            #         plots.append(features.data)
            #         feature_list.append(features)
            #         continue
            #     feature_list.append(features)
            #     features = [features]
            #


        pdfWriter = PdfWriter()
        pdfWriter.create_pdf_report(feature_list, plots, dataset_count_dict, self.output_path + "report.pdf")
