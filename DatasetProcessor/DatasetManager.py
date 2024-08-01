from ConfigReader import ConfigReader
from utils import ClassNamesDict
from PdfWriter import PdfWriter
from DatasetProcessor import DatasetInfo
from FeatureAnalysis import FeatureSummary


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
        self.features2compare = config_processor.get_features_2_compare()

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

    def _build_feature_sum_2_compare(self, feature_name, feature_summaries):
        features_list = []
        for feauture_sum in feature_summaries:
            features_list.extend(feauture_sum.get_feature_list())
        new_feature_sum = FeatureSummary.FeatureSummary(feature_name, features_list, feature_tag="Compare")
        return new_feature_sum

    def run(self):
        self._read_config()
        name_summary_dict = {}
        for feature_name, visual_methods in self.features.items():
            plots = []
            if not self._check_info_4_feature(feature_name):
                print(f"No info for this feature: {feature_name}")
                continue

            feature_analyzer = ClassNamesDict.AnalysersClassNamesDict[feature_name](self.dataset_info)
            featureSummary = feature_analyzer.get_feature()
            featureSummary.set_visual_methods(visual_methods)

            for visual_method in visual_methods:
                visualizer = ClassNamesDict.VisualizersClassNamesDict[visual_method]()
                plots.append(visualizer.visualize(featureSummary))
            featureSummary.set_plots(plots)
            name_summary_dict[feature_name] = featureSummary
            self.featureSummaries.append(featureSummary)

        if self.features2compare is not None:
            for features2comp_names, features2comp_data in self.features2compare.items():
                plots = []
                feature1_name, feature2_name = features2comp_data["features"][0], features2comp_data["features"][1]
                feature1 , feature2 = name_summary_dict.get(feature1_name, None), name_summary_dict.get(feature2_name, None)
                if feature1 is None or feature2 is None:
                    print("No necessary features above")
                    continue
                featureSummaryComp = self._build_feature_sum_2_compare(features2comp_names, [feature1, feature2])
                visual_methods = features2comp_data["visualization_methods"]
                for visual_method in visual_methods:
                    visualizer = ClassNamesDict.VisualizersClassNamesDict[visual_method]()
                    plots.append(visualizer.visualize(featureSummaryComp))
                featureSummaryComp.set_plots(plots)
                self.featureSummaries.append(featureSummaryComp)

        pdfWriter = PdfWriter(self.featureSummaries, self.dataset_info, self.output_path + "report.pdf")
        pdfWriter.write()
