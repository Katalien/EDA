from typing import List
from Visualizer.VisualizeSetiings import VisualizeSettings
from utils.FeatureMetadata import VisualizersClassNamesDict
from FeatureSummaryData import ClassFeatureData


class FeatureSummary:
    """
    Class with full data, plots and description about one specific feature for images and masks of all classes in dataset.
    Class combines all information about given feature, visualize it and save plots

    Attributes:
         feature_name (str): Name of the current feature
         features_list (list): List of ClassFeatureData objects.
                            One ClassFeatureData object contains feature information for one specific class.
                            FeatureSummary object combines information on all classes for a given feature.
         feature_tag (str): Tag for feature (see utils.FeatureMetadata):
                            - 'General' feature contains information of overall image (ex. image brightness)
                            - 'Labels' feature contains information about masks and objects in dataset
                            (ex. Classes frequency, ClassesArea)
                            - 'Masks' feature contains feature's values inside masks (ex. MaskedContrast)
                            - 'Compare' feature combines information for visualizing feature values for further comparison
        is_img_feature (bool): True if data is represented in the form of a plot. False if data is a list of values
        visual_methods_name (list): List of names for feature visualization.
        plots (list): List of final plots of given feature
        description (str): FeatureSummary object description. This description will be shown in final report
        visual_settings (VisualizeSettings): VisualSettings object which contains information for correct visualization
    """
    def __init__(self,
                 feature_name,
                 features: List,
                 feature_tag=None,
                 visual_settings: VisualizeSettings = None,
                 description: str = None,
                 visual_methods_names=None):
        """
        Initialize FeatureSummary Object
        :param feature_name: Name of a given feature
        :param features: List of ClassFeatureData objects
        :param feature_tag: Tag for given feature ('General', 'Masks', 'Labels', 'Compare')
        :param visual_settings: VisualSettings object for correct plots visualization
        :param description: Description for given feature
        """
        self.feature_name: str = feature_name
        self.features_list: List = self.__set_features(features)
        self.is_img_feature: bool = self.__is_img_feature()
        self.visual_methods_name: List | None = visual_methods_names
        self.plots = []
        self.description = description
        self.visual_settings = visual_settings
        self.feature_tag = feature_tag
        if self.feature_tag not in ["General", "Labels", "Masks", "Compare"] and self.feature_tag is not None:
            raise ValueError("Invalid tag")

    @classmethod
    def from_dict(cls, data_dict):
        class_features_list = []
        for class_feature_dict in data_dict["features_list"]:
            class_feature_item = ClassFeatureData.ClassFeatureData.from_dict(class_feature_dict)
            class_features_list.append(class_feature_item)
        feature_name = data_dict.get("feature_name", None)
        feature_tag = data_dict.get("feature_tag", None)
        description = data_dict.get("description", None)
        visual_methods_names = data_dict.get("visual_methods_name", None)
        visual_settings = data_dict.get("visual_settings", None)
        instance = cls(feature_name,
                       class_features_list,
                       feature_tag=feature_tag,
                       description=description,
                       visual_settings=visual_settings,
                       visual_methods_names=visual_methods_names)
        instance.visualize(visual_methods_names)
        return instance

    def __repr__(self):
        return f"Feature Summary\n Feature: {self.feature_name}\n"

    def set_visual_methods(self, vis_methods):
        self.visual_methods_name = vis_methods

    def set_description(self, description):
        self.description = description

    def set_plots(self, plots):
        self.plots = plots

    def set_is_img_feature(self, _is_img_feature):
        self.is_img_feature = _is_img_feature

    def __is_img_feature(self):
        return True if self.features_list[0].is_img else False

    def __set_features(self, features):
        return features if isinstance(features, List) else [features]

    def get_feature_list(self):
        return self.features_list

    def visualize(self, visual_methods):
        if self.is_img_feature:
            return
        try:
            self.visual_methods_name = visual_methods
            for visual_method in self.visual_methods_name:
                visualizer = VisualizersClassNamesDict[visual_method]()
                plot = visualizer.visualize(self)
                self.plots.append(plot)
        except Exception as e:
            print(f"Error {e}")




