from .Feature import Feature
from typing import Dict
import cv2

class Class2ImageRatioFeature(Feature):
    def calculate(self, sample) -> Dict:
        mask_val_dict = {}
        for mask_class in sample.get_all_mask_classes():
            mask = sample.load_mask(mask_class)
            value = self.calculate_objects_per_image(mask)
            mask_val_dict[mask_class] = value
        return mask_val_dict

    def calculate_objects_per_image(self, mask):
        ratios = []
        image_area = mask.shape[0] * mask.shape[1]
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area != 0:
                ratio = area / image_area
                ratios.append(ratio)
        return ratios