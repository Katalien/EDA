import cv2
import numpy as np
from FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.FeatureData import FeatureData
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from DatasetProcessor import DatasetInfo
from .LabeledFeatures import LabeledFeatures
from PIL import Image


class LocationsMap(LabeledFeatures):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.feature_name = "Object location map"
        self.weight = 1
        self.image_shape = self._get_image_size()
        self.dict_res_maps = {}
        self.weight = 0.5

    def _process_dataset(self):
        super()._process_dataset()

        fig_dict = {}
        for key, val in self.classes_frequency.items():
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
        # plt.show()

        return self.figure_to_array(fig)

    def figure_to_array(self, fig):
        # Draw the figure on the canvas
        canvas = FigureCanvas(fig)
        canvas.draw()

        # Get the RGBA buffer from the figure
        buf = canvas.buffer_rgba()

        # Convert to a NumPy array
        image = np.asarray(Image.frombuffer('RGBA', canvas.get_width_height(), buf, 'raw', 'RGBA', 0, 1))

        # Convert RGBA to RGB (remove alpha channel)
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

        return image

    def get_feature(self):
        self._process_dataset()
        feature = FeatureData(self.feature_name, self.dict_res_maps, is_img=True)
        return feature

    def show_image(self, image, name):
        im = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
        cv2.imshow(name, im)
        cv2.waitKey()

