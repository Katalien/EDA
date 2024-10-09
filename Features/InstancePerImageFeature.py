from .Feature import Feature
from typing import Dict
import cv2

class InstancePerImageFeature(Feature):
    def calculate(self, sample) -> Dict:
        mask_val_dict = {}
        for mask_class in sample.get_all_mask_classes():
            mask = sample.load_mask(mask_class)
            value = self.calculate_objects_per_image(mask)
            mask_val_dict[mask_class] = value
        return mask_val_dict

    def calculate_objects_per_image(self, mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return len(contours)