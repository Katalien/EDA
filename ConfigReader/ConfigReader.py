import yaml
import os
from typing import Dict, Any, List, Union

class ConfigReader:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        with open(self.config_path, 'r') as file:
            return yaml.safe_load(file)

    def get_images_path(self) -> str:
        return self.config.get('images_path', None)

    def get_dataset_path(self) -> str:
        return self.config.get('dataset_path', None)

    def get_labels_path(self) -> str:
        return self.config.get('labels_path', None)

    def get_prediction_path(self) -> str:
        return self.config.get('predictions_path', None)

    def get_masks_path(self) -> str:
        return self.config.get('masks_path', None)

    def get_output_path(self) -> str:
        return self.config.get('output_path', "./")

    def get_general_features(self) -> Union[Dict[str, List[str]], None]:
        general_features = self.config.get("General_features", None)
        if general_features is None:
            return None
        return {feature: methods["visualization_methods"] for feature, methods in general_features.items()}

    def get_labeled_features(self) -> Union[Dict[str, List[str]], None]:
        labeled_features = self.config.get("Labeled_features", None)
        if labeled_features is None:
            return None
        return {feature: methods["visualization_methods"] for feature, methods in labeled_features.items()}

    def get_predicted_features(self) -> Union[Dict[str, List[str]], None]:
        predicted_features = self.config.get("Predicted_features", None)
        if predicted_features is None:
            return None
        return {feature: methods["visualization_methods"] for feature, methods in predicted_features.items()}

    def get_features(self):
        features = self.config.get("Features", None)
        return {feature: methods["visualization_methods"] for feature, methods in features.items()}

