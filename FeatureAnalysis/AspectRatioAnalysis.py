from .FeatureAnalysis import FeatureAnalysis
from PIL import Image
import numpy as np

class AspectRatioAnalysis(FeatureAnalysis):
    def extract(self, image: Image.Image) -> float:
        return image.width / image.height