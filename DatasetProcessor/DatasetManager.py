# вызывает датасет процессор для всех фичей

import os
from typing import Dict, List
from utils import buildFeatures, ClassNamesDict
from DatasetFeatureProcessor import DatasetFeatureProcessor
from FeatureAnalysis import Feature

class DatasetManager:
    def __init__(self, dataset_path: str, output_path: str, features_config: Dict[str, List[str]]):
        self.dataset_path = dataset_path
        self.output_path = output_path
        self.features_config = features_config
        self.dataset_features = []

    def manage(self):
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        features2analyse = buildFeatures(self.features_config)
        analyzers = list(features2analyse.keys())
        for analyzer in analyzers:
            dataset_processor = DatasetFeatureProcessor(self.dataset_path, analyzer)
            feature = dataset_processor.get_feature()
            feature.set_visual_methods(features2analyse.keys())
            self.dataset_features.append(feature)

