from typing import List
import numpy as np

class ClassFeatureData:
    """
    Class keeps information about one specific feature and class for all samples in dataset
    For general image features (ex. overall brightness, contrast etc.) class_name is "General".

    Attributes:
        feature_name (str): Name of the current feature.
        self.class_name (str): Name of the current class. 'General' class for images features.
        self.data ( dict[str, list] | np.ndarray):
                        This attribute can either be a dictionary with feature values
                        for all samples in the dataset or a final plot represented as a NumPy array.
                        - If `dict`: Contains the information to visualize plot.
                        Keys: 'x', 'y'
                        Values: values for x and y axis
                        - If `np.ndarray`: Represents the final plot data as a 2D or 3D array.
        self.min (float | int): Min value in data list. 'None' if data is a plot.
        self.max (float | int): Max value in data list.'None' if data is a plot.
        self.mean (float | int): Mean of data list. 'None' if data is a plot.
        self.std (float | int): Standard diviation of data list. 'None' if data is a plot.
        self.is_img (bool): True if data is a plot (np.ndarray). False otherwise.
    """
    def __init__(self, feature_name: str,
                 data: dict | np.ndarray,
                 class_name: str = "General",
                 _min: float | int = None,
                 _max: float | int = None,
                 _mean: float | int = None,
                 _std: float | int = None,
                 is_img: bool = False):
        self.feature_name: str = feature_name
        self.data: dict | np.ndarray = data
        self.class_name: str = class_name
        self.min: float | int = _min
        self.max: float | int = _max
        self.mean: float | int = _mean
        self.std: float | int = _std
        self.is_img: bool = is_img

    @classmethod
    def from_dict(cls, data_dict):
        feature_name = data_dict["feature_name"]
        class_name = data_dict["class_name"]
        data = data_dict["data"]
        _min = data_dict.get("min", None)
        _max = data_dict.get("max", None)
        _mean = data_dict.get("mean", None)
        _std = data_dict.get("std", None)
        is_img = data_dict.get("is_img", None)
        return cls(feature_name, data, class_name, _min=_min, _max=_max, _std=_std, _mean=_mean, is_img=is_img )

    def __repr__(self):
        return f"Class FeatureData: \n " \
               f"Feature name: {self.feature_name}\n" \
               f"Class name: {self.class_name}\n"
