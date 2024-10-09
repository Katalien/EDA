from typing import Dict, List



# new one
class Sample:
    def __init__(self, image_path: str, class_path:str|Dict, feature_list:list):
        self.image_path: str = image_path
        self.class_path: str = class_path
        self.active_features = {}
        for feature in feature_list:
            self.active_features[feature] = None


    def fill_features_info(self):
        for feature in self.active_features.keys():
            print()

    def get_feature_info(self, feature_name):
        pass

