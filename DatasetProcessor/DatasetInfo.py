import os
import cv2
from typing import List, Dict, Set

DatasetClasses = {
    "sco": "border chip",
    "top": "border face"
}

class DatasetInfo:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.images_path: List = []
        self.masks_path: Dict[str, List] = {}
        self.prediction_path = None
        self.images_count = None
        self.masks_count: Dict[str, int] = {}
        self.image_size = None
        self.mask_size = None
        self.fill_info()

    def _get_image_size(self, filepath):
        print("haha", filepath)
        image = cv2.imread(filepath)
        return image.shape

    def _get_all_files(self):
        image_files = []
        deepest_directories = []

        for root, dirs, files in os.walk(self.dataset_path):
            root = root.replace("\\", "/")
            if not dirs:
                current_images = []
                for file in files:
                    file_path = os.path.join(root, file)
                    file_path = file_path.replace("\\", "/")
                    if os.path.isfile(file_path):
                        current_images.append(file_path)
                if current_images:
                    image_files.extend(current_images)
                    deepest_directories.append(root)
        return image_files, deepest_directories

    def fill_info(self):
        all_paths, files_dirs = self._get_all_files()
        for i, dir_path in enumerate(files_dirs):
            for image_name in os.listdir(dir_path):

                filepath = os.path.join(dir_path, image_name)
                filepath = filepath.replace("\\", "/")
                # исходное изображение
                if len(image_name.split("_")) == 1:
                    self.images_path.append(filepath)
                # маска
                else:
                    image_class = image_name.split("_")[1].split(".")[0]
                    class_name = DatasetClasses[image_class]
                    if class_name not in self.masks_path:
                        self.masks_path[class_name] = []
                        self.masks_path[class_name].append(filepath)
                    else:
                        self.masks_path[class_name].append(filepath)

        self.images_count = len(self.images_path)
        self.image_size = self._get_image_size(self.images_path[0])
        self.mask_size = self._get_image_size(list(self.masks_path.values())[0][0])
        for key, val in self.masks_path.items():
            self.masks_count[key] = len(list(val))





