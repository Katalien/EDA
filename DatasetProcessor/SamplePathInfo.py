class SamplePathInfo:
    """
    Class with the information about one sample's image and masks path.
    One image can have different masks with different tags
    """
    def __init__(self, image_path: str, classes_paths: dict):
        self.__image_path: str = image_path
        self.__classes_path = classes_paths

    def set_class_path(self, class_name, mask_path):
        if class_name not in self.__classes_path:
            self.__classes_path[class_name] = mask_path

    def get_image_path(self):
        return self.__image_path

    def get_mask_path_by_tag(self, class_name):
        return self.__classes_path[class_name]

    def get_mask_path_dict(self):
        return self.__classes_path
