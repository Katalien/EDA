from .Feature import Feature
from typing import Dict
import cv2


class ClassesDiameterFeature(Feature):
    def calculate(self, sample) -> Dict:
        mask_val_dict = {}
        for mask_class in sample.get_all_mask_classes():
            if mask_class == "General":
                continue
            contours = sample.get_contours_by_class(mask_class)
            value = ClassesDiameterFeature.calculate_diameters(contours)
            mask_val_dict[mask_class] = value
        return mask_val_dict

    @staticmethod
    def calculate_diameters(contours):
        diameters = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            diameter = w if w > h else h
            diameters.append(diameter)
        return diameters
