from abc import ABC, abstractmethod
from PIL import Image
from typing import Any, Dict
import numpy as np


class FeatureExtractor(ABC):
    @abstractmethod
    def extract(self, image: Image.Image) -> Any:
        pass

class BrightnessExtractor(FeatureExtractor):
    def extract(self, image: Image.Image) -> float:
        img_array = np.array(image)
        return np.mean(img_array)

class ContrastExtractor(FeatureExtractor):
    def extract(self, image: Image.Image) -> float:
        img_array = np.array(image)
        return np.std(img_array)

class AspectRatioExtractor(FeatureExtractor):
    def extract(self, image: Image.Image) -> float:
        return image.width / image.height