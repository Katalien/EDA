from .Feature import Feature
from typing import Dict
import cv2

class ClassesDiameterFeature(Feature):
    def calculate(self, sample) -> Dict:
        mask_val_dict = {}
        for mask_class in sample.get_all_mask_classes():
            if mask_class == "General":
                continue
            mask = sample.load_mask(mask_class)
            value = self.calculate_diameters(mask)
            mask_val_dict[mask_class] = value
        return mask_val_dict

    def calculate_diameters(self, mask):
        diameters = []
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            diameter = w if w > h else h
            diameters.append(diameter)
        return diameters
