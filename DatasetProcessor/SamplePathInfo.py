class SamplePathInfo():
    def __init__(self, image_path):
        self.__image_path = image_path
        self.__classes_path = {}

    def set_all_classes_path(self, class_path_dict):
        self.__classes_path = class_path_dict

    def set_class_path(self, class_name, mask_path):
        if class_name not in self.__classes_path:
            self.__classes_path[class_name] = mask_path

    def get_image_path(self):
        return self.__image_path

    def get_mask_path_by_tag(self, class_name):
        return self.__classes_path[class_name]

    def get_mask_path_dict(self):
        return self.__classes_path
