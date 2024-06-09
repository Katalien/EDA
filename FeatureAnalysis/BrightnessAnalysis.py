from .FeatureAnalysis import FeatureAnalysis
from PIL import Image
import numpy as np

class BrightnessAnalysis(FeatureAnalysis):
    def extract(self, image: Image.Image) -> float:
        img_array = np.array(image)
        return np.mean(img_array)