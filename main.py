from DatasetProcessor import DatasetManager
import time

# TODO сбилдить фичи для сравнения маскированных объектов и фона вцелом
# TODO добавить медианную яркость
# TODO добавить градиент по всему изображению
# TODO Correlation Matrix: Correlation between different features (e.g., pixel intensities, object sizes).
# TODO Local Feature Descriptors: Histogram of oriented gradients (HOG), SIFT, or other local feature descriptors.
# проверить нули в таблицах
# карта градиента? объединить


# добавить обработку ошибок: конциг ридер
# заменить все на подсчет numpy
# добавить сохранение мета файла и построение по мета файлу
# добавить описание фичей
# добавить паралельное вычисление
# убрать лог с исключением фичей
if __name__ == "__main__":
    start = time.time()
    manager = DatasetManager.DatasetManager("./config/config.yaml")
    manager.run_()
    print(time.time() - start)










