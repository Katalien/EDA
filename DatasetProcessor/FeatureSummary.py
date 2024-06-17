class FeatureSummary:
    def __init__(self, feature_name, features, visual_method_name="", plots=None):
        self.feature_name = feature_name
        self.features = features
        self.visual_method_name = visual_method_name
        self.plots = plots
        self.description = f"{visual_method_name} of {feature_name}"

    def set_plots(self, plots):
        self.plots = plots


