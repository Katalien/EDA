from .Feature import Feature
from typing import Dict
import cv2
import numpy as np


class MaskedBrightnessFeature(Feature):
    def calculate(self, sample) -> Dict:
        image = sample.load_image()
        mask_val_dict = {}
        for mask_class in sample.get_all_mask_classes():
            if mask_class == "General":
                continue
            mask = sample.load_mask(mask_class)
            contours = sample.get_contours_by_class(mask_class)
            value = MaskedBrightnessFeature.calculate_masked_brightness(image, mask, contours)
            mask_val_dict[mask_class] = value
        return mask_val_dict

    @staticmethod
    def calculate_masked_brightness(image, mask, contours):
        values = []
        for contour in contours:
            if cv2.contourArea(contour) > 3:
                cur_mask = np.zeros_like(mask)
                cur_mask = cv2.drawContours(cur_mask, [contour], -1, (255, 255, 255), -1)
                masked_pixels = image[cur_mask == 255]
                values.append(np.mean(masked_pixels))
        return values
