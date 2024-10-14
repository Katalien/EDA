import numpy as np

from ConfigReader import ConfigReader
from FeatureAnalysis.ClassFeatureData import ClassFeatureData
from utils import ClassNamesDict
from PdfWriter import PdfWriter
from DatasetProcessor import DatasetInfo
from FeatureAnalysis import FeatureSummary
from .SamplePathInfo import SamplePathInfo
from .Sample import Sample
from typing import Dict
from Features import LocationMapBuilder
from tqdm import tqdm


GeneralFeatures = ["AspectRatio", "Brightness", "Color", "Contrast"]
LabeledFeatures = ["ClassesFrequency", "InstancesPerImage", "LocationMap", "ClassesArea",
                   "ClassesBbAspectRatio", "ClassesDiameter", "Class2ImageRatio"]
MaskedFeatures = ["MaskedContrast", "MaskedBrightness", "MaskedGradient"]
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
        self.extensions_dict = {}

    def _read_config(self):
        config_processor = ConfigReader(self.config_path)
        self.dataset_path = config_processor.get_dataset_path()
        self.output_path = config_processor.get_output_path()
        self.classes = config_processor.get_classes()
        extensions_dict = config_processor.get_extensions()
        self.dataset_info = DatasetInfo.DatasetInfo(self.dataset_path, self.classes, extensions_dict)
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

    def __get_feature_tag(self, feature_name):
        if feature_name in GeneralFeatures:
            return "General"
        if feature_name in LabeledFeatures:
            return "Labels"
        if feature_name in MaskedFeatures:
            return "Masks"
    #     compare

    def __build_feature_class(self, feature_name, data_list, class_name):
        data = np.array(data_list)
        _min = data.min()
        _max = data.max()
        _std = data.std()
        _mean = data.mean()
        data_dict = {"x": len(data), "y": data}
        feature = ClassFeatureData(feature_name,
                                   data_dict,
                                   class_name=class_name,
                                   _min=_min,
                                   _max=_max,
                                   _mean=_mean,
                                   _std=_std)
        return feature

    def __build_feature_summary(self, feature_name, class_names, all_feature_values):
        features = []
        for class_name in class_names:
            class_values = []
            for sample_val in all_feature_values:
                if class_name in list(sample_val.keys()):
                    if isinstance(sample_val[class_name], list):
                        class_values.extend(sample_val[class_name])
                    elif isinstance(sample_val[class_name], int) or isinstance(sample_val[class_name], float):
                        class_values.append(sample_val[class_name])
            if len(class_values) != 0:
                feature = self.__build_feature_class(feature_name, class_values, class_name)
                features.append(feature)

        return FeatureSummary.FeatureSummary(feature_name,
                                             features,
                                             feature_tag=self.__get_feature_tag(feature_name))

    def __process_locations_map(self, dataset_info):
        loc_map_builder = LocationMapBuilder.LocationsMapBuilder(dataset_info)
        return loc_map_builder.get_feature()

    def run_(self):
        all_samples = []
        self._read_config()

        for sample_path_item in tqdm(self.dataset_info.get_samples_path_info(), desc="Count features for all samples"):
            feature_sample = Sample(sample_path_item, self.features.keys())
            feature_sample.fill_features_info()
            all_samples.append(feature_sample)

        all_classes = all_samples[0].get_all_mask_classes()
        feature_summaries_dict = {}

        for feature_name, visual_methods in self.features.items():
            if feature_name == "LocationsMap":
                loc_map_feature_summary = self.__process_locations_map(self.dataset_info)
                self.featureSummaries.append(loc_map_feature_summary)
                feature_summaries_dict[feature_name] = loc_map_feature_summary
            else:
                all_feature_values = []
                for sample in tqdm(all_samples, desc=f"Process {feature_name} feature"):
                    feature_val_dict = sample.get_feature_val_by_feature_name(feature_name)
                    all_feature_values.append(feature_val_dict)
                feature_summary = self.__build_feature_summary(feature_name, all_classes, all_feature_values)
                feature_summary.visualize(visual_methods)
                print(feature_summary.feature_tag)
                feature_summaries_dict[feature_name] = feature_summary
                self.featureSummaries.append(feature_summary)
        pdfWriter = PdfWriter(self.featureSummaries, self.dataset_info, self.output_path + "report_new_arch.pdf")
        pdfWriter.write()


