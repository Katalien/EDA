from typing import List
from Visualizer.VisualizeSetiings import VisualizeSettings
from utils.FeatureMetadata import VisualizersClassNamesDict


class FeatureSummary:
    def __init__(self, feature_name, features, feature_tag=None, visual_settings: VisualizeSettings = None):
        self.feature_name: str = feature_name
        self.features_list: List = self._set_features(features)
        self.is_img_feature: bool = self._is_img_feature()
        self.visual_methods_name: List = None
        self.plots = []
        self.description = None
        self.visual_settings = visual_settings
        self.feature_tag = feature_tag
        if self.feature_tag not in ["General", "Labels", "Attributes", "Masks", "Compare"] and self.feature_tag is not None:
            raise ValueError("Invalid tag")

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

    def _is_img_feature(self):
        return True if self.features_list[0].is_img else False

    def _set_features(self, features):
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




