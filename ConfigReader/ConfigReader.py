import yaml
from typing import Dict, Any


class ConfigReader:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        with open(self.config_path, 'r') as file:
            return yaml.safe_load(file)

    def get_dataset_path(self) -> str:
        return self.config.get('dataset_path', None)

    def get_output_path(self) -> str:
        return self.config.get('output_path', "./")

    def get_features(self):
        features = self.config.get("Features", None)
        return {feature: methods["visualization_methods"] for feature, methods in features.items()}

    def get_features_2_compare(self):
        return self.config.get("CompareFeatures", None)

    def get_classes(self):
        return self.config.get("Classes", None)

    def get_extensions(self):
        extensions = self.config.get("Ext", None)
        if extensions is not None:
            return {"image_ext": extensions["image_ext"], "mask_ext": extensions["mask_ext"]}

