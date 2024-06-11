from PIL import Image
from typing import List, Dict, Type, Any
from FeatureAnalysis import FeatureAnalysis

class ImageProcessor:
    def __init__(self, image: Image.Image, extractors: List[Type[FeatureAnalysis]]):
        self.image = image
        self.extractors = [extractor() for extractor in extractors]

    def __extract_features(self) -> Dict[str, Any]:
        features = {}
        for extractor in self.extractors:
            feature_name = extractor.__class__.__name__.replace("Analysis", "")
            features[feature_name] = extractor.extract(self.image)
        return features

    def get_image_features(self) -> Dict[str, Dict[str, Any]] :
        return self.__extract_features()

