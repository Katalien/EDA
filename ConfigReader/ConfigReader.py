import yaml
import os
from typing import Dict, Any, List, Type

class ConfigReader:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        with open(self.config_path, 'r') as file:
            return yaml.safe_load(file)

    def get_images_path(self) -> str:
        return self.config.get('images_path', '')

    def get_output_path(self) -> str:
        path = self.config.get('output_path', None)
        if path is None:
            path = "../../reports/"
        return path

    def get_features_config(self) -> Dict[str, List[str]]:
        config_features = self.config.get('features', {})
        map_features = {feature: methods["visualization_methods"] for feature, methods in config_features.items()}
        print(map_features)
        return map_features
