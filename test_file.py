import cv2
import os
import matplotlib.pyplot as plt
import numpy as np


# def _get_all_files(dataset_path):
#     image_files = []
#     deepest_directories = []
#
#     for root, dirs, files in os.walk(dataset_path):
#         root = root.replace("\\", "/")
#         if not dirs:
#             current_images = []
#             for file in files:
#                 file_path = os.path.join(root, file)
#                 file_path = file_path.replace("\\", "/")
#                 if os.path.isfile(file_path):
#                     current_images.append(file_path)
#             if current_images:
#                 image_files.extend(current_images)
#                 deepest_directories.append(root)
#     return image_files, deepest_directories
#
#
# def fill_info(dataset_path):
#     images_path = []
#     all_paths, files_dirs = _get_all_files(dataset_path)
#     for i, dir_path in enumerate(files_dirs):
#         for image_name in os.listdir(dir_path):
#
#             filepath = os.path.join(dir_path, image_name)
#             filepath = filepath.replace("\\", "/")
#
#             # исходное изображение
#             if len(image_name.split("_")) == 1:
#                 images_path.append(filepath)
#     return images_path
#
#
# dataset_path = "../dataset/real_dataset/"
# red, green, blue = None, None, None
# images_dirs = fill_info(dataset_path)
# for image_dir in images_dirs:
#     image = cv2.imread(image_dir)
#     colors = ("red", "green", "blue")
#     for channel_id, color in enumerate(colors):
#         histogram, bin_edges = np.histogram(
#             image[:, :, channel_id], bins=256, range=(0, 256)
#         )

import numpy as np
import matplotlib.pyplot as plt

# Количество бинов
bins = 256

# Генерация данных для убывающей гистограммы
hist_data_descending = np.linspace(100, 0, bins)
data_descending = np.repeat(range(bins), hist_data_descending.astype(int))

# Генерация данных для гистограммы с постоянным значением
constant_value = 50
hist_data_constant = np.full(bins, constant_value)
data_constant = np.repeat(range(bins), hist_data_constant.astype(int))

# Визуализация
fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# Гистограмма с убывающими значениями
axes[0, 0].hist(data_descending, bins=bins, color='blue', edgecolor='black')
axes[0, 0].set_title('Histogram with Descending Values')
axes[0, 0].set_xlabel('Bins')
axes[0, 0].set_ylabel('Frequency')

# Гистограмма с постоянным значением
axes[0, 1].hist(data_constant, bins=bins, color='red', edgecolor='black')
axes[0, 1].set_title('Histogram with Constant Value')
axes[0, 1].set_xlabel('Bins')
axes[0, 1].set_ylabel('Frequency')

# Создание массивов для гистограмм
hist_descending, _ = np.histogram(data_descending, bins=bins, range=(0, bins))
hist_constant, _ = np.histogram(data_constant, bins=bins, range=(0, bins))

# Сложение массивов поэлементно
hist_sum = hist_descending + hist_constant

# Вычисление среднего значений гистограмм
hist_mean = (hist_descending + hist_constant) / 2

# Визуализация гистограммы суммы
axes[1, 0].hist(range(bins), bins=bins, weights=hist_sum, color='green', edgecolor='black')
axes[1, 0].set_title('Sum of Histograms')
axes[1, 0].set_xlabel('Bins')
axes[1, 0].set_ylabel('Frequency')

# Визуализация среднего значений гистограмм
axes[1, 1].hist(range(bins), bins=bins, weights=hist_mean, color='purple', edgecolor='black')
axes[1, 1].set_title('Mean of Histograms')
axes[1, 1].set_xlabel('Bins')
axes[1, 1].set_ylabel('Frequency')

plt.tight_layout()
plt.show()