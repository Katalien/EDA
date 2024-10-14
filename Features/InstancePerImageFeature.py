from .Feature import Feature
from typing import Dict


class InstancePerImageFeature(Feature):
    def calculate(self, sample) -> Dict:
        mask_val_dict = {}
        for mask_class in sample.get_all_mask_classes():
            if mask_class == "General":
                continue
            contours = sample.get_contours_by_class(mask_class)
            mask_val_dict[mask_class] = len(contours)
        return mask_val_dict
