import cv2
import numpy as np
from DatasetProcessor import DatasetInfo
from .MaskedFeatures import MaskedFeatures
from FeatureAnalysis import FeatureSummary

class MaskedContrastAnalysis(MaskedFeatures):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.grayscale = True
        self.feature_name = "Masked Contrast"

    def _process_one_sample(self, image: np.ndarray, mask: np.ndarray):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        values = []
        for contour in contours:
            if cv2.contourArea(contour) > 3:
                cur_mask = np.zeros_like(mask)
                cur_mask = cv2.drawContours(cur_mask, [contour], -1, 255, -1)
                masked_pixels = image[cur_mask == 255]
                values.append(np.std(masked_pixels))
        return values

    def get_feature(self) -> FeatureSummary:
        super().get_feature()
        self.summary.set_description(f"Masked segments contrast analysis")
        return self.summary
    def show(self, image, name=""):
        sample = cv2.resize(image, (0, 0), fx=0.3, fy=0.3)
        cv2.imshow(name, sample)
        cv2.waitKey()