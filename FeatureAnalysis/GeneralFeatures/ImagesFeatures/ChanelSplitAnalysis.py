import random
import cv2
import numpy as np
from FeatureAnalysis.ClassFeatureData import ClassFeatureData
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from PIL import Image
from DatasetProcessor import DatasetInfo
from .ImagesFeatures import ImagesFeatures
from FeatureAnalysis import FeatureSummary


class ChanelSplitAnalysis(ImagesFeatures):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.feature_name = "Chanel split"
        self.dict_res_figs = {"RGB FORMAT": [], "HLS FORMAT": [], "YCbCr FORMAT": []}

    def _process_dataset(self):
        file_dirs = self.dataset_info.images_path
        random_image_path = random.choice(file_dirs)
        image = cv2.imread(random_image_path)
        fig_rgb, fig_hls, fig_ycbcr = self._process_one_sample(image)
        self.dict_res_figs["RGB FORMAT"] = fig_rgb
        self.dict_res_figs["HLS FORMAT"] = fig_hls
        self.dict_res_figs["YCbCr FORMAT"] = fig_ycbcr

    def _process_one_sample(self, sample: np.ndarray):
        image_rgb = cv2.cvtColor(sample, cv2.COLOR_BGR2RGB)
        r = image_rgb[:, :, 0]
        g = image_rgb[:, :, 1]
        b = image_rgb[:, :, 2]
        fig_rgb = self.get_plots([r, g, b], ["red", "green", "blue"], suptitle="RGB channels")

        image_hls = cv2.cvtColor(sample, cv2.COLOR_BGR2HLS)
        h = image_hls[:, :, 0]
        l = image_hls[:, :, 1]
        s = image_hls[:, :, 2]
        fig_hls = self.get_plots([h, l, s], ["hue", "lightness", "saturation"], suptitle="HLS channels")

        image_ycbcr = cv2.cvtColor(sample, cv2.COLOR_BGR2YCrCb)
        y = image_ycbcr[:, :, 0]
        cb = image_ycbcr[:, :, 1]
        cr = image_ycbcr[:, :, 2]
        fig_ycbcr = self.get_plots([y, cb, cr], ["Luminance", "Chrominance-Blue", "Chrominance-Red"], suptitle="YCbCr channels")

        return fig_rgb, fig_hls, fig_ycbcr

    def _get_image_size(self):
        filepath = list(self.dataset_info.masks_path.values())[0][0]
        im = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        return im.shape

    def get_feature(self) -> FeatureSummary:
        self._process_dataset()
        features = []
        for im_format, figs in self.dict_res_figs.items():
            feature = ClassFeatureData(self.feature_name,
                                       figs,
                                       class_name=im_format,
                                       is_img=True)
            features.append(feature)
        self.summary = FeatureSummary.FeatureSummary(self.feature_name, features, feature_tag="General")
        self.summary.set_description("Splitting a random image by channels in 3 formats: RGB, HLS, YCbCr")
        return self.summary

    def get_plots(self, images, titles=None, suptitle="", bgr2rgb=True):
        cols = len(images)
        new_images = []
        if titles is None:
            titles = [""] * len(images)
        if bgr2rgb:
            for image in images:
                new_images.append(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            images = new_images

        fig = plt.figure(figsize=(12, 12))

        for i, (image, title) in enumerate(zip(images, titles)):
            ax = fig.add_subplot(cols, 1, i + 1)
            ax.imshow(image)
            ax.axis('off')
            ax.set_title(title, fontsize=20, fontweight='bold')

        # fig.suptitle(suptitle)
        plt.tight_layout()  # Улучшает автоматическое размещение подграфиков
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