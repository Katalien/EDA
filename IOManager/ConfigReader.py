import yaml
from typing import Dict, Any


class ConfigReader:
    """
    Class for parsing config file
    """
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        with open(self.config_path, 'r') as file:
            return yaml.safe_load(file)

    def get_dataset_path(self) -> str:
        dataset_path = self.config.get('Dataset Path', None)
        if dataset_path is None:
            raise ValueError("The 'Dataset Path' field is required in config file")
        return dataset_path

    def get_output_path(self) -> str:
        return self.config.get('Output Path', "./")

    def get_features(self) -> dict:
        features = self.config.get("Features", None)
        if features is None:
            raise ValueError("The 'Features' field is required in config file")
        return {feature: methods["visualization_methods"] for feature, methods in features.items()}

    def get_features_2_compare(self):
        return self.config.get("CompareFeatures", None)

    def get_classes(self):
        return self.config.get("Classes", {})

    def get_extensions(self):
        extensions = self.config.get("Ext", None)
        if extensions is not None:
            return {"image_ext": extensions["image_ext"], "mask_ext": extensions["mask_ext"]}
        else:
            return {"image_ext": "tiff", "mask_ext": "tiff"}

    def get_save_json_info(self):
        save_json = self.config.get("Save Json", None)
        return save_json

