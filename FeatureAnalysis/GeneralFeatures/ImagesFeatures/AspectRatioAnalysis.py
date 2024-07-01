import numpy as np
from DatasetProcessor import DatasetInfo
from .ImagesFeatures import ImagesFeatures
from ... import FeatureSummary


class AspectRatioAnalysis(ImagesFeatures):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.feature_name = "Aspect Ratio"

    def _process_one_sample(self, sample: np.ndarray):
        height, width = sample.shape[:2]
        return width / height

    def get_feature(self) -> FeatureSummary:
        super().get_feature()
        self.summary.set_description("Overall aspect ratio for all images in the dataset")
        return self.summary


