import os
import json
import cv2
import numpy as np
import pandas as pd
from FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.FeatureData import FeatureData
from DatasetProcessor import FileIterator
from utils import Classes


class LocationsMap(FeatureAnalysis):
    def __init__(self, labels_path: str):
        super().__init__(labels_path)
        self.path = labels_path
        self.feature_name = "Object location map"
        self.dict_res_maps = {}
        self.weight = 1
        self.image_shape = -1

    def _process_dataset(self):
        image_files, file_dirs = FileIterator.get_images_from_lowest_level_folders(self.path)
        self.image_shape = self._get_image_size(image_files[0])
        sample_count = len(image_files)
        self.weight = 1
        for i, dir_path in enumerate(file_dirs):
            for image_name in os.listdir(dir_path):
                if len(image_name.split("_")) != 1:  # skip original image
                    class_name = image_name.split("_")[1].split(".")[0]
                    if class_name not in list(Classes.DatasetClasses.keys()):
                        print(f"Unkwown class in {dir_path}, no class {class_name}")
                        continue
                    filepath = os.path.join(os.path.normpath(dir_path), image_name)
                    filepath = filepath.replace("\\", "/")
                    image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
                    self._process_one_sample(image, class_name)

    def _process_one_sample(self, sample: str, class_name: str):
        dict_class_name = Classes.DatasetClasses[class_name]
        if dict_class_name not in self.dict_res_maps:
            mask = np.zeros(shape=self.image_shape, dtype=np.uint8)
            res_mask = cv2.addWeighted(mask, 1, sample, self.weight, 0)
            self.dict_res_maps[dict_class_name] = res_mask
        else:
            cur_mask = self.dict_res_maps[dict_class_name]
            res_mask = cv2.addWeighted(cur_mask, 1, sample, self.weight, 0)
            self.dict_res_maps[dict_class_name] = res_mask

    def _get_image_size(self, image_path):
        filepath = os.path.join(image_path)
        im = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        return im.shape

    def get_feature(self):
        self._process_dataset()
        feature = FeatureData(self.feature_name, self.dict_res_maps, is_img=True)
        return feature

    def show_image(self, image, name):
        im = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
        cv2.imshow(name, im)
        cv2.waitKey()

