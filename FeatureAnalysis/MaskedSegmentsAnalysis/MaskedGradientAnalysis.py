import cv2
import numpy as np
from DatasetProcessor import DatasetInfo
from .MaskedFeatures import MaskedFeatures

class MaskedGradientAnalysis(MaskedFeatures):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.grayscale = True
        self.feature_name = "Masked Gradient"

    def _process_one_sample(self, image: np.ndarray, mask: np.ndarray):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        values =[]
        for contour in contours:
            cur_mask = np.zeros_like(mask)
            cur_mask = cv2.drawContours(cur_mask, [contour], 0, 255, -1)
            masked_pixels = image[cur_mask == 255]
            values.append(cv2.Laplacian(masked_pixels, cv2.CV_64F).var())
        return values
