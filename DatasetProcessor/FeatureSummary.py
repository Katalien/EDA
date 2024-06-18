from typing import List

class FeatureSummary:
    def __init__(self, feature_name, features, visual_method_name="", plots=None):
        self.feature_name = feature_name
        self.features_list = self._set_features(features)
        self.is_img_feature = self._is_img_feature()
        self.visual_method_name = visual_method_name
        self.plots = plots
        self.description = f"{visual_method_name} of {feature_name}"

    def set_plots(self, plots):
        self.plots = plots

    def _is_img_feature(self):
        return True if self.features_list[0].is_img else False

    def _set_features(self, features):
        return features if isinstance(features, List) else [features]




