class GuiInfo():
    def __init__(self):
        self.images_path = None
        self.labels_path = None
        self.masks_path = None
        self.prediction_path = None
        self.features = None
        self.output_path = None

    def set_images_path(self, path):
        self.images_path = path

    def set_labels_path(self, path):
        self.labels_path = path

    def set_masks_path(self, path):
        self.masks_path = path

    def set_predictions_path(self, path):
        self.prediction_path = path

    def set_output_path(self, path):
        self.output_path = path

    def set_features(self, features):
        print("set features")
        for feature in features:
            self.features[feature] = {"visualization_methods": ['default']}
        print(self.features)
