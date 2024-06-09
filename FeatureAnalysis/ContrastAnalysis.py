from .FeatureAnalysis import FeatureAnalysis
from PIL import Image
import numpy as np

class ContrastAnalysis(FeatureAnalysis):
    def extract(self, image: Image.Image) -> float:
        img_array = np.array(image)
        return np.std(img_array)