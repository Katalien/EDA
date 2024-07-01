from abc import ABC, abstractmethod
from typing import Any
from DatasetProcessor import DatasetInfo


class FeatureAnalysis(ABC):

    def __init__(self, dataset_info: DatasetInfo):
        self.dataset_info = dataset_info

    @abstractmethod
    def _process_dataset(self) :
        pass

    @abstractmethod
    def _process_one_sample(self,  *args: Any, **kwargs: Any):
        pass

    @abstractmethod
    def get_feature(self):
        pass