import cv2
import numpy as np
from FeatureSummaryData.ClassFeatureData import ClassFeatureData
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from DatasetProcessor import DatasetInfo
from PIL import Image
from FeatureSummaryData import FeatureSummary


class LocationsMapBuilder:
    def __init__(self, dataset_info: DatasetInfo):
        self.dataset_info = dataset_info
        self.feature_name = "Object location map"
        self.dict_res_maps = {}
        self.image_shape = self.__get_image_size()
        self.classes = set()
        self.summary: FeatureSummary = None

    def __process_dataset(self):
        sample_paths_items = self.dataset_info.get_samples_path_info()

        for sample_path_item in sample_paths_items:
            masks_path = sample_path_item.get_mask_path_dict()
            for class_name, path in masks_path.items():
                mask = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                self.__process_one_sample(mask, class_name)

        fig_dict = {}
        for key, val in self.dict_res_maps.items():
            val = val * (255 // self.dataset_info.masks_count[key])
            fig_dict[key] = LocationsMapBuilder.__get_plt(val, bgr2rgb=True)

        self.dict_res_maps = fig_dict

    def __process_one_sample(self, sample, class_name):
        sample = cv2.resize(sample, (self.image_shape[1], self.image_shape[0]), interpolation=cv2.INTER_LINEAR)
        if class_name not in self.dict_res_maps:
            mask = np.zeros(shape=self.image_shape, dtype=np.uint8)
            mask += (sample // 255)
            self.dict_res_maps[class_name] = mask
        else:
            cur_mask = self.dict_res_maps[class_name]
            cur_mask += (sample // 255)
            self.dict_res_maps[class_name] = cur_mask

    def __get_image_size(self):
        if self.dataset_info.equal_mask_sizes:
            filepath = list(self.dataset_info.masks_path.values())[0][0]
            im = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
            return im.shape
        else:
            return 800, 800

    @staticmethod
    def __get_plt(image, bgr2rgb=False, bgr2gray=False):
        image_height, image_width = image.shape
        aspect_ratio = image_width / image_height

        fig_height = 12
        fig_width = fig_height * aspect_ratio

        fig = plt.figure(figsize=(fig_width, fig_height))
        if bgr2rgb:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if bgr2gray:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        plt.imshow(image)
        plt.axis('off')

        return LocationsMapBuilder.__figure_to_array(fig)

    @staticmethod
    def __figure_to_array(fig):
        canvas = FigureCanvas(fig)
        canvas.draw()
        buf = canvas.buffer_rgba()
        image = np.asarray(Image.frombuffer('RGBA', canvas.get_width_height(), buf, 'raw', 'RGBA', 0, 1))
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        return image

    def get_feature(self):
        self.__process_dataset()
        features = []
        for key, plot in self.dict_res_maps.items():
            feature = ClassFeatureData(self.feature_name, plot, class_name=key, is_img=True)
            features.append(feature)
        self.summary = FeatureSummary.FeatureSummary(self.feature_name, features, feature_tag="Labels")
        self.summary.set_is_img_feature(True)
        self.summary.set_description("Locations map for different classes")
        return self.summary

