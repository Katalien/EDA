from DatasetProcessor import DatasetManager

# добавить сохранение мета файла и построение по мета файлу
# добавить паралельное вычисление
if __name__ == "__main__":
    manager = DatasetManager.DatasetManager("./config/config.yaml")
    # manager.run()
    manager.run_from_json("./meta.json", "../reports/report_from_json.pdf")






