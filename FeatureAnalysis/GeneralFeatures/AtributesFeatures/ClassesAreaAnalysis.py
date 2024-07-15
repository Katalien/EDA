import cv2
import numpy as np
from FeatureAnalysis import FeatureAnalysis
from FeatureAnalysis.ClassFeatureData import ClassFeatureData
from DatasetProcessor import DatasetInfo
from FeatureAnalysis import FeatureSummary
from typing import Dict, List
from .AtributesFeatures import AtributesFeatures
import matplotlib.pyplot as plt

class ClassesAreaAnalysis(AtributesFeatures):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.feature_name = "Area (pxls)"


    def _process_one_sample(self, sample: np.ndarray,  class_name:str):
        contours, _ = cv2.findContours(sample, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area != 0:
                if str(class_name) not in list(self.classes_attr_dict.keys()):
                    self.classes_attr_dict[class_name] = [area]
                else:
                    self.classes_attr_dict[class_name].append(area)

    def get_feature(self) -> FeatureSummary:
        super().get_feature()
        self.summary.set_description("Square of classes segments, pxls")
        return self.summary

    def show(self, image, name=""):
        sample = cv2.resize(image, (0, 0), fx=0.3, fy=0.3)
        cv2.imshow(name, sample)
        cv2.waitKey()

    def show_plots(self, cols, images, titles, bgr2rgb=True):
        new_images = []
        if bgr2rgb:
            for image in images:
                new_images.append(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            images = new_images
        for i, image_title in enumerate(zip(images, titles)):
            image = image_title[0]
            title = image_title[1]
            plt.subplot(1, cols, i + 1)  # 1 строка, 2 столбца, позиция 1
            plt.imshow(image)
            plt.axis('off')
            plt.title(title)
        plt.show()

    def show_plt(self, image, title="image", bgr2rgb=False, bgr2gray=False):
        if bgr2rgb:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if bgr2gray:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        plt.imshow(image)
        plt.axis('off')
        plt.title(title)
        plt.show()
