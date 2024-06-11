# обрабатывает одну метрику для всего датасета
# возвращает экземпляр Фича с описанием одной метрики для всего датасета
import os
from typing import List
from ..utils import ClassNamesDict
import ImageFeatureProcessor
import cv2

class DatasetFeatureProcessor:
    def __init__(self, dataset_path:str, feature_name:str, visual_methods_name:List[str]):
        self.dataset_path = dataset_path
        self.feature_name = feature_name
        self.feature_analyzer = ClassNamesDict.ClassNamesDict[feature_name]
        # self.processor = ImageProcessor(self.feature_analyzer)
        self.data = []

    def __process_dataset(self):
        for filename in os.listdir(self.dataset_path):
            image = cv2.imread(filename)
            self.data.append(ImageFeatureProcessor.ImageFeatureProcessor.analyze(self.feature_analyzer, image))

    def get_feature(self):
        self.__process_dataset()
