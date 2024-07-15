from DatasetProcessor import DatasetManager


# TODO сбилдить фичи для сравнения маскированных объектов и фона вцелом
# TODO добавить медианную яркость
# TODO добавить градиент по всему изображению
# TODO Correlation Matrix: Correlation between different features (e.g., pixel intensities, object sizes).
# TODO Local Feature Descriptors: Histogram of oriented gradients (HOG), SIFT, or other local feature descriptors.
# проверить нули в таблицах
# карта градиента? объединить


if __name__ == "__main__":
    manager = DatasetManager.DatasetManager("./config/config.yaml")
    manager.run()











