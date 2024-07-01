from typing import Dict, List
import os
import re


def buildFeatures(features_config: Dict[str, List]) -> Dict[str, List]:
    features2analyze = {}
    for key, val in features_config.items():
        capitalKey = key.capitalize() + "Analysis"
        features2analyze[capitalKey] = list(val)
    return features2analyze

def parse_image_path( path):
    dir_path = os.path.dirname(path)
    filename = os.path.basename(path)
    filename_no_ext, file_extension = os.path.splitext(filename)
    match = re.match(r'(\d+)_([a-z]+)', filename_no_ext)
    if match:
        image_number = match.group(1)
        class_type = match.group(2)
        return dir_path, image_number, class_type, file_extension
    else:
        raise ValueError("Неверный формат имени файла")

def mask_path2image_path(mask_path):
    dir_path, image_number, class_type, file_ext = parse_image_path(mask_path)
    possible_extensions = [".tif", ".tiff", ".png", ".jpg"]

    for ext in possible_extensions:
        image_path = f"{dir_path}/{image_number}{ext}"
        if os.path.exists(image_path):
            return image_path