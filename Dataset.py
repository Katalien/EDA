from typing import List, Type, Dict
import os
from PIL import Image
import FeatureExtractor
from ImageProcessor import ImageProcessor

IMG_EXTENSIONS = (
    "jpeg",
    "jpg",
    "png",
    "tif",
    "tiff",
)

class DatasetProcessor():
    def __init__(self, images_path: str, extractors: List[Type[FeatureExtractor]]):
        self.images_path = images_path
        self.extractors = extractors
        self.images_features = []

    def process_dataset(self):
        for file in os.listdir(self.images_path):
            if file.split(".")[-1] in IMG_EXTENSIONS:
                image = Image.open(os.path.join(self.images_path, file))
                processor = ImageProcessor(file, image, self.extractors)
                map_image_features = processor.get_image_features()
                self.images_features.append(map_image_features)
