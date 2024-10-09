from .Feature import Feature
from typing import Dict
import cv2

class ClassesBBAspectRatioFeature(Feature):
    def calculate(self, sample) -> Dict:
        mask_val_dict = {}
        for mask_class in sample.get_all_mask_classes():
            mask = sample.load_mask(mask_class)
            value = self.calculate_bb_aspect_ratio(mask)
            mask_val_dict[mask_class] = value
        return mask_val_dict

    def calculate_bb_aspect_ratio(self, mask):
        bb_aspect_ratios = []
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h
            bb_aspect_ratios.append(aspect_ratio)
        return bb_aspect_ratios
