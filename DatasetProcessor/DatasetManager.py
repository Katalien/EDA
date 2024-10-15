import numpy as np
from IOManager import ConfigReader, PdfWriter, JsonWriter, JsonReader
from FeatureAnalysis.ClassFeatureData import ClassFeatureData
from utils.FeatureMetadata import VisualizersClassNamesDict, FeatureDescriptions
from DatasetProcessor import DatasetInfo
from FeatureAnalysis import FeatureSummary
from .Sample import Sample
from Features import LocationMapBuilder, ClassesFrequencyBuilder, ColorHistogramBuilder
from tqdm import tqdm
from utils.FeatureMetadata import GeneralFeatures, LabeledFeatures, MaskedFeatures


class DatasetManager:
    """
    Main class for processing dataset and manage all analysis work
    """
    def __init__(self, config_path: str = "./config.yaml"):
        self.config_path = config_path
        self.featureSummaries = []
        self.classes = None
        self.dataset_path = None
        self.output_path = None
        self.dataset_info = None
        self.dataset_classes = None
        self.extensions_dict = {}

    def __read_config(self):
        config_processor = ConfigReader(self.config_path)
        self.dataset_path = config_processor.get_dataset_path()
        self.output_path = config_processor.get_output_path()
        self.classes = config_processor.get_classes()
        extensions_dict = config_processor.get_extensions()
        self.dataset_info = DatasetInfo.DatasetInfo(self.dataset_path, self.classes, extensions_dict)
        self.features = config_processor.get_features()
        self.features2compare = config_processor.get_features_2_compare()

    @staticmethod
    def __build_feature_summary_2_compare(feature_name, feature_summaries):
        features_list = []
        for feature_sum in feature_summaries:
            features_list.extend(feature_sum.get_feature_list())
        new_feature_sum = FeatureSummary.FeatureSummary(feature_name, features_list, feature_tag="Compare")
        return new_feature_sum

    @staticmethod
    def __get_feature_tag(feature_name):
        if feature_name in GeneralFeatures:
            return "General"
        if feature_name in LabeledFeatures:
            return "Labels"
        if feature_name in MaskedFeatures:
            return "Masks"

    @staticmethod
    def __build_class_feature_data(feature_name, data_list, class_name):
        data = np.array(data_list)
        _min = np.min(data)
        _max = np.max(data)
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

    @staticmethod
    def __build_feature_summary(feature_name, class_names, all_feature_values):
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
                feature = DatasetManager.__build_class_feature_data(feature_name, class_values, class_name)
                features.append(feature)

        return FeatureSummary.FeatureSummary(feature_name,
                                             features,
                                             feature_tag=DatasetManager.__get_feature_tag(feature_name),
                                             description=FeatureDescriptions[feature_name])

    def __process_locations_map(self):
        loc_map_builder = LocationMapBuilder.LocationsMapBuilder(self.dataset_info)
        return loc_map_builder.get_feature()

    def __process_color_histogram(self):
        color_hist_builder = ColorHistogramBuilder.ColorHistogramBuilder(self.dataset_info)
        return color_hist_builder.get_feature()

    def __process_classes_frequency(self):
        class_freq_builder = ClassesFrequencyBuilder.ClassesFrequencyBuilder(self.dataset_info)
        return class_freq_builder.get_feature()

    def __fill_samples_info(self):
        all_samples = []
        sample_path_items = self.dataset_info.get_samples_path_info()
        for sample_path_item in tqdm(sample_path_items, desc="Count features for all samples"):
            feature_sample = Sample(sample_path_item, list(self.features.keys()))
            all_samples.append(feature_sample)
        return all_samples

    def __fill_feature_summaries_info(self, all_samples, all_classes):
        feature_summaries_dict = {}
        for feature_name, visual_methods in self.features.items():
            if feature_name == "LocationsMap":
                feature_summary = self.__process_locations_map()
            elif feature_name == "ClassesFrequency":
                feature_summary = self.__process_classes_frequency()
            elif feature_name == "Color":
                feature_summary = self.__process_color_histogram()
            else:
                all_feature_values = []
                for sample in tqdm(all_samples, desc=f"Process {feature_name} feature"):
                    feature_val_dict = sample.get_feature_val_by_feature_name(feature_name)
                    all_feature_values.append(feature_val_dict)
                feature_summary = DatasetManager.__build_feature_summary(feature_name, all_classes, all_feature_values)
            feature_summary.visualize(visual_methods)
            feature_summaries_dict[feature_name] = feature_summary
            self.featureSummaries.append(feature_summary)
        return feature_summaries_dict

    def __fill_feature2compare_info(self, feature_summaries_dict):
        for features2comp_names, features2comp_data in self.features2compare.items():
            try:
                plots = []
                feature1_name = features2comp_data["features"][0]
                feature2_name = features2comp_data["features"][1]
                feature1 = feature_summaries_dict.get(feature1_name, None)
                feature2 = feature_summaries_dict.get(feature2_name, None)
                if feature1 is None or feature2 is None:
                    raise ValueError(f"Missing features: {feature1_name}, {feature2_name}")

                feature_summary_comp = DatasetManager.__build_feature_summary_2_compare(features2comp_names,
                                                                                        [feature1, feature2])
                visual_methods = features2comp_data["visualization_methods"]
                for visual_method in visual_methods:
                    visualizer = VisualizersClassNamesDict[visual_method]()
                    plots.append(visualizer.visualize(feature_summary_comp))
                feature_summary_comp.set_plots(plots)
                self.featureSummaries.append(feature_summary_comp)
            except ValueError as e:
                print(f"Error: {e}. Skipping this comparison and continuing.")
                continue

    def run_from_json(self, json_filepath, save_filepath):
        json_reader = JsonReader.JsonReader(json_filepath)
        dataset_info, feature_summaries = json_reader.read_json()
        pdf_writer = PdfWriter(feature_summaries, dataset_info, save_filepath)
        pdf_writer.write()

    def run(self):
        self.__read_config()
        all_samples = self.__fill_samples_info()

        all_classes = list(self.classes.keys())
        all_classes.append("General")

        feature_summaries_dict = self.__fill_feature_summaries_info(all_samples, all_classes)
        if self.features2compare is not None:
            self.__fill_feature2compare_info(feature_summaries_dict)

        pdf_writer = PdfWriter(self.featureSummaries, self.dataset_info, self.output_path)
        pdf_writer.write()
        jsonWriter = JsonWriter(self.featureSummaries, self.dataset_info, "./meta.json")
        jsonWriter.save_feature_summary_to_json()



