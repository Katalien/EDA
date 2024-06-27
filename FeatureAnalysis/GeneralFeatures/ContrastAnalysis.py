from DatasetProcessor import DatasetInfo
from .GeneralFeatures import GeneralFeatures
import numpy as np


class ContrastAnalysis(GeneralFeatures):
    def __init__(self, dataset_info: DatasetInfo):
        super().__init__(dataset_info)
        self.feature_name = "Contrast"


    def _process_one_sample(self, sample: np.ndarray):
        return np.std(sample)


