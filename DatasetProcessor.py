from typing import List, Type, Dict
import os
from PIL import Image
from ImageProcessor import ImageProcessor
from FeatureAnalysis import FeatureAnalysis

IMG_EXTENSIONS = (
    "jpeg",
    "jpg",
    "png",
    "tif",
    "tiff",
)

class DatasetProcessor():
    def __init__(self, images_path: str, extractors: List[Type[FeatureAnalysis]]):
        self.images_path = images_path
        self.extractors = extractors
        self.images_features = []
        self.features = self.__get_features_name()
        self.dataset_features = self.__create_dataset_features_map()

    def __process_dataset(self):
        for file in os.listdir(self.images_path):
            if file.split(".")[-1] in IMG_EXTENSIONS:
                image = Image.open(os.path.join(self.images_path, file))
                processor = ImageProcessor(image, self.extractors)
                map_features = processor.get_image_features()
                self.images_features.append({file: map_features})
                for key, value in self.dataset_features.items():
                    self.dataset_features[key].append(map_features[key])
        return self.dataset_features

    def get_features(self):
        return self.__process_dataset()

    def __get_features_name(self):
        features = []
        for extractor in self.extractors:
            # print(extractor().__class__.__name__)
            feature_name = extractor().__class__.__name__.replace("Analysis", "")
            if feature_name != 'ABCMeta':
                features.append(feature_name)
        return features

    def __create_dataset_features_map(self):
        dataset_features = {}
        for feature_name in self.features:
            dataset_features[feature_name] = []
        return dataset_features


