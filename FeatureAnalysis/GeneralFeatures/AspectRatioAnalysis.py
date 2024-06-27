import numpy as np
from DatasetProcessor import DatasetInfo
from .GeneralFeatures import GeneralFeatures

class AspectRatioAnalysis(GeneralFeatures):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.feature_name = "Aspect Ratio"


    def _process_one_sample(self, sample: np.ndarray):
        height, width = sample.shape[:2]
        return width / height


