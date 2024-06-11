from .FeatureAnalysis import FeatureAnalysis
from PIL import Image
import numpy as np

class BrightnessAnalysis(FeatureAnalysis):
    def extract(self, image: np.ndarray) -> float:
        return np.mean(image)