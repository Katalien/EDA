from .Feature import Feature
from typing import Dict
import cv2

class ClassesAreaFeature(Feature):
    def calculate(self, sample) -> Dict:
        mask_val_dict = {}
        for mask_class in sample.get_all_mask_classes():
            if mask_class == "General":
                continue
            contours = sample.get_contours_by_class(mask_class)
            value = self.calculate_objects_per_image( contours)
            mask_val_dict[mask_class] = value
        return mask_val_dict

    def calculate_objects_per_image(self, contours):
        return [cv2.contourArea(cnt) for cnt in contours]
