from .FeatureAnalysis import FeatureAnalysis
from PIL import Image
import numpy as np

class AspectRatioAnalysis(FeatureAnalysis):
    def extract(self, image: np.ndarray) -> float:
        height, width = image.shape[:2]
        return width / height