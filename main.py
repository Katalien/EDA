from DatasetProcessor import DatasetManager

# добавить сохранение мета файла и построение по мета файлу
# добавить паралельное вычисление
if __name__ == "__main__":
    manager = DatasetManager.DatasetManager("./config/config.yaml")
    manager.run()








