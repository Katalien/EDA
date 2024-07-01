import cv2
import numpy as np
from ... import FeatureSummary
from FeatureAnalysis.ClassFeatureData import ClassFeatureData
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from DatasetProcessor import DatasetInfo
from .LabelesFeatures import LabelesFeatures
from PIL import Image


class LocationsMap(LabelesFeatures):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.feature_name = "Object location map"
        self.dict_res_maps = {}
        self.weight = 1
        self.image_shape = self._get_image_size()

    def _process_dataset(self):
        file_dirs_dict = self.dataset_info.masks_path
        sample_count = len(file_dirs_dict)
        self.weight = 1
        for i, (class_name, paths) in enumerate(file_dirs_dict.items()):
            for filepath in paths:
                image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
                self._process_one_sample(image, class_name)

        fig_dict = {}
        for key, val in self.dict_res_maps.items():
            fig_dict[key] = self.get_plt(val, title=key)
        self.dict_res_maps = fig_dict

    def _process_one_sample(self, sample: str, class_name: str):
        if class_name not in self.dict_res_maps:
            mask = np.zeros(shape=self.image_shape, dtype=np.uint8)
            res_mask = cv2.addWeighted(mask, 1, sample, self.weight, 0)
            self.dict_res_maps[class_name] = res_mask
        else:
            cur_mask = self.dict_res_maps[class_name]
            res_mask = cv2.addWeighted(cur_mask, 1, sample, self.weight, 0)
            self.dict_res_maps[class_name] = res_mask

    def _get_image_size(self):
        filepath = list(self.dataset_info.masks_path.values())[0][0]
        im = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        return im.shape

    def get_plt(self, image, title="", bgr2rgb=False, bgr2gray=False):
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
        plt.title(title)

        return self.figure_to_array(fig)

    def figure_to_array(self, fig):
        canvas = FigureCanvas(fig)
        canvas.draw()
        buf = canvas.buffer_rgba()
        image = np.asarray(Image.frombuffer('RGBA', canvas.get_width_height(), buf, 'raw', 'RGBA', 0, 1))
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        return image

    def get_feature(self) -> FeatureSummary:
        self._process_dataset()
        features = []
        for key, plt in self.dict_res_maps.items():
            feature = ClassFeatureData(self.feature_name,
                                       plt,
                                       class_name=key,
                                        is_img=True)
            features.append(feature)
        self.summary = FeatureSummary.FeatureSummary(self.feature_name, features)
        self.summary.set_is_img_feature(True)
        self.summary.set_description("Locations map for different classes")

        return self.summary

    def show_image(self, image, name):
        im = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
        cv2.imshow(name, im)
        cv2.waitKey()