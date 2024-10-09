# import os
# import cv2
# from typing import List, Dict, Set
# import utils.utils as ut
#
# class SamplePathInfo():
#     def __init__(self, image_path):
#         self.image_path = image_path
#         self.classes_path = {}
#
#     def set_class_path(self, class_name, mask_path):
#         if class_name not in self.classes_path:
#             self.classes_path[class_name] = mask_path
#
# class DatasetInfoOld:
#     def __init__(self, dataset_path, classes_dict):
#         self.dataset_path = dataset_path
#         self.dataset_classes = classes_dict
#         self.images_path: List = []
#         self.masks_path: Dict[str, List] = {}
#         self.prediction_path = None
#         self.images_count = None
#         self.masks_count: Dict[str, int] = {}
#         self.image_sizes: Set = set()
#         self.mask_sizes: Set = set()
#         self.equal_image_sizes = False
#         self.equal_mask_sizes = False
#         self.samples_path_info_list = []
#         self.fill_info()
#
#     def _fill_image_size(self, filepath):
#         if filepath.split(".")[-1] == "psd":
#             image = ut.get_np_from_psd(filepath)
#         else:
#             image = cv2.imread(filepath)
#         self.image_sizes.add(image.shape)
#
#
#     def _fill_mask_size(self, filepath):
#         mask = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
#         if mask is not None:
#             self.mask_sizes.add(mask.shape)
#
#
#     def _get_all_files(self):
#         image_files = []
#         deepest_directories = []
#
#         for root, dirs, files in os.walk(self.dataset_path):
#             root = root.replace("\\", "/")
#             if not dirs:
#                 current_images = []
#                 for file in files:
#                     file_path = os.path.join(root, file)
#                     file_path = file_path.replace("\\", "/")
#                     if os.path.isfile(file_path):
#                         current_images.append(file_path)
#                 if current_images:
#                     image_files.extend(current_images)
#                     deepest_directories.append(root)
#         return image_files, deepest_directories
#
#
#     def fill_info(self):
#         all_paths, files_dirs = self._get_all_files()
#         for i, dir_path in enumerate(files_dirs):
#             for image_name in os.listdir(dir_path):
#
#                 filepath = os.path.join(dir_path, image_name)
#                 filepath = filepath.replace("\\", "/")
#
#                 # исходное изображение
#                 if len(image_name.split("_")) == 1:
#                     self.images_path.append(filepath)
#                     self._fill_image_size(filepath)
#
#                 # маска
#                 else:
#                     self._fill_mask_size(filepath)
#                     image_class = image_name.split("_")[1].split(".")[0]
#                     class_name = self.dataset_classes[image_class]
#
#                     if image_class not in list(self.dataset_classes.keys()):
#                         print(image_class)
#                         continue
#                     if class_name not in self.masks_path:
#                         self.masks_path[class_name] = []
#                         self.masks_path[class_name].append(filepath)
#                     else:
#                         self.masks_path[class_name].append(filepath)
#
#
#         self.images_count = len(self.images_path)
#         self.equal_image_sizes = True if len(self.image_sizes) == 1 else False
#         self.equal_mask_sizes = True if len(self.mask_sizes) == 1 else False
#         print("images", self.equal_image_sizes)
#         print("masks", self.equal_mask_sizes)
#
#         for key, val in self.masks_path.items():
#             self.masks_count[key] = len(list(val))
#
#
#
#
