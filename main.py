import numpy as np
import cv2
import os
from FeatureExtractor import BrightnessExtractor, ContrastExtractor, AspectRatioExtractor

if __name__ == "__main__":
    extractors = [BrightnessExtractor, ContrastExtractor, AspectRatioExtractor]
    dataset_processor = DatasetProcessor('path/to/images', extractors)
    features_list = dataset_processor.process_dataset()

    for features in features_list:
        print(features)