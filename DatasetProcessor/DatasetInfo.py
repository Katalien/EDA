import os
import cv2
from typing import List, Dict, Set
import utils.utils as ut
from .SamplePathInfo import SamplePathInfo
from tqdm import tqdm


class DatasetInfo:
    """
    Class for keeping and managing information about images and masks in dataset

    Attributes:
        dataset_path (str): Path to directory with dataset. Set in the configuration file.
        dataset_classes (dict): Dictionary with masks of dataset. Set in the configuration file.
                                    Key: mask tag in filename (ex. _mask),
                                    Value: name of the class in final report
        extensions_dict (dict[str, str]): Dictionary with extensions of images and masks. Set in the configuration file.
        images_path: (list): List with all images paths
        masks_path: (dict): Dictionary with masks paths.
                            Key: name (tag) of the class
                            Value: List of the masks paths with this tag
        images_count (int): Total amount of images in dataset
        masks_count (Dict[str, int]): Total amount of masks in dataset.
                                     Key: name (tag) of the class
                                     Value: amount of masks with this tag
        image_sizes (set): Set of all images sizes
        mask_sizes (set):Set of all masks sizes
        equal_image_sizes (bool): Show if all images in dataset have the same shape
        equal_mask_sizes (bool): Show if all masks in dataset have the same shape
        __samples_path_info_list (list[SamplePathInfo]): List with SamplePathInfo objects

    """
    def __init__(self, dataset_path, classes_dict, extensions, fillInfo = True):
        """
        Initializes the DatasetInfo object.

        Args:
           dataset_path (str): Path to the directory containing the dataset.
           classes_dict (dict): Dictionary mapping mask tags to class names for the final report.
           extensions (dict[str, str]): Dictionary of file extensions for images and masks.

        """
        self.dataset_path = dataset_path
        self.dataset_classes = classes_dict
        self.extensions_dict = extensions
        self.images_path: List = []
        self.masks_path: Dict[str, List] = {}
        self.images_count = 0
        self.masks_count: Dict[str, int] = {}
        self.image_sizes: Set = set()
        self.mask_sizes: Set = set()
        self.equal_image_sizes = False
        self.equal_mask_sizes = False
        self.__samples_path_info_list = []
        self.dataset_classes["General"] = "General"
        if fillInfo:
            self.__fill_info()

    @classmethod
    def from_dict(cls, data: dict):
        """
        Creates an instance of DatasetInfo from a dictionary.

        Args:
            data (dict): Dictionary containing the dataset information.

        Returns:
            DatasetInfo: An instance of the DatasetInfo class.
        """
        dataset_path = data.get('dataset_path', '')
        classes_dict = data.get('dataset_classes', {})
        instance = cls(dataset_path, classes_dict, {}, fillInfo=False)
        instance.images_count = data.get('images_count', 0)
        instance.masks_count = data.get('masks_count', {})
        instance.equal_image_sizes = data.get('equal_image_sizes', False)
        instance.equal_mask_sizes = data.get('equal_mask_sizes', False)
        return instance

    def get_final_class_name_by_tag(self, tag):
        return self.dataset_classes[tag]

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

    def __update_mask_count(self, tag):
        if tag not in self.masks_count:
            self.masks_count[tag] = 1
        else:
            self.masks_count[tag] += 1

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
            self.__update_mask_count(tag)
            mask_path = mask_path.replace("\\", "/")
            masks_path_dict[tag] = mask_path
        return masks_path_dict

    def __fill_info(self):
        image_filepaths, deepest_directories = self.__get_all_files_and_dirs()
        for filepath in tqdm(image_filepaths, desc="Fill info about dataset"):
            if not self.__is_mask(filepath):
                masks_path_dict = self.__get_masks_by_image_name(filepath)
                sample_info = SamplePathInfo(filepath, masks_path_dict)
                self.__fill_image_size(filepath)
                self.__samples_path_info_list.append(sample_info)
                self.images_count += 1
                self.images_path.append(filepath)

        self.equal_image_sizes = True if len(self.image_sizes) == 1 else False
        self.equal_mask_sizes = True if len(self.mask_sizes) == 1 else False

        for key, val in self.masks_path.items():
            self.masks_count[key] = len(list(val))

    def get_samples_path_info(self):
        return self.__samples_path_info_list

    def get_images_paths(self):
        return self.images_path
