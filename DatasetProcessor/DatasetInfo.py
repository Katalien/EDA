import os
import cv2
from typing import List, Dict, Set
import utils.utils as ut

class SamplePathInfo():
    def __init__(self, image_path):
        self.__image_path = image_path
        self.__classes_path = {}

    def set_all_classes_path(self, class_path_dict):
        self.__classes_path = class_path_dict

    def set_class_path(self, class_name, mask_path):
        if class_name not in self.__classes_path:
            self.__classes_path[class_name] = mask_path

    def get_image_path(self):
        return self.__image_path

    def get_mask_path_by_tag(self, class_name):
        return self.__classes_path[class_name]

    def get_mask_path_dict(self):
        return self.__classes_path


class DatasetInfo():
    def __init__(self, dataset_path, classes_dict, extensions):
        self.dataset_path = dataset_path
        self.dataset_classes = classes_dict
        self.extensions_dict = extensions
        self.images_path: List = []
        self.masks_path: Dict[str, List] = {}

        self.images_count = None
        self.masks_count: Dict[str, int] = {}
        self.image_sizes: Set = set()
        self.mask_sizes: Set = set()
        self.equal_image_sizes = False
        self.equal_mask_sizes = False
        self.samples_path_info_list = []
        self.__fill_info()

    def __fill_image_size(self, filepath):
        if filepath.split(".")[-1] == "psd":
            image = ut.get_np_from_psd(filepath)
        else:
            image = cv2.imread(filepath)
        if image is None:
            raise ValueError(f"Image is None. Filepath {filepath}")
        self.image_sizes.add(image.shape)


    def __fill_mask_size(self, filepath):
        mask = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        if mask is not None:
            self.mask_sizes.add(mask.shape)
        else:
            raise ValueError(f"Image is None. Filepath {filepath}")

    def __get_all_files_and_dirs(self):
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


    def __is_mask(self, path):
        image_name = os.path.basename(path)
        for tag in self.dataset_classes:
            if tag in image_name:
                return True
        return False

    def __get_masks_by_image_name(self, image_path):
        masks_path_dict = {}
        dir_name = os.path.dirname(image_path)
        image_name = os.path.basename(image_path).split(".")[0]
        for tag in self.dataset_classes:
            mask_path_with_name = os.path.join(dir_name, image_name)
            mask_path = mask_path_with_name + f"_{tag}.{self.extensions_dict['mask_ext']}"
            if not os.path.exists(mask_path):
                continue
            self.__fill_mask_size(mask_path)
            mask_path = mask_path.replace("\\", "/")
            masks_path_dict[tag] = mask_path
        return masks_path_dict




    def __fill_info(self):
        image_filepaths, deepest_directories = self.__get_all_files_and_dirs()
        # все файлы в одной директории
        if len(deepest_directories) == 1:
            for filepath in image_filepaths:
                if not self.__is_mask(filepath):
                    sample_info = SamplePathInfo(filepath)
                    self.__fill_image_size(filepath)
                    masks_path_dict = self.__get_masks_by_image_name(filepath)
                    sample_info.set_all_classes_path(masks_path_dict)
                    self.samples_path_info_list.append(sample_info)

        # все файлы в разных директориях
        else:
            for filepath in image_filepaths:
                if not self.__is_mask(filepath):
                    sample_info = SamplePathInfo(filepath)
                    masks_path_dict = self.__get_masks_by_image_name(filepath)
                    sample_info.set_all_classes_path(masks_path_dict)
                    self.samples_path_info_list.append(sample_info)

        self.images_count = len(self.images_path)
        self.equal_image_sizes = True if len(self.image_sizes) == 1 else False
        self.equal_mask_sizes = True if len(self.mask_sizes) == 1 else False
        print("images", self.equal_image_sizes)
        print("masks", self.equal_mask_sizes)

        for key, val in self.masks_path.items():
            self.masks_count[key] = len(list(val))

