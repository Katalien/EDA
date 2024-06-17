import cv2
import os
import matplotlib.pyplot as plt
import numpy as np

# # Путь к папке с изображениями
# folder_path = "../dataset/tiny_coco_images/"
#
# image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png', '.jpeg'))]
#
# # Цвета для графиков
# colors = ('b', 'g', 'r')
# channel_hist = {color: np.zeros(256) for color in colors}
#
# # Проходим по каждому файлу
# for file in image_files:
#     # Полный путь к текущему изображению
#     file_path = os.path.join(folder_path, file)
#
#     # Считываем изображение
#     img = cv2.imread(file_path)
#
#     # Считаем гистограммы для каждого цветового канала
#     for i, col in enumerate(colors):
#         histr = cv2.calcHist([img], [i], None, [256], [0, 256])
#         channel_hist[col] += histr.flatten()
#
# # Нормализуем гистограммы
# for color in colors:
#     channel_hist[color] /= channel_hist[color].sum()
#
# # Строим график
# plt.figure(figsize=(10, 6))
#
# for col in colors:
#     plt.plot(range(256), channel_hist[col], color=col)
#     plt.xlim([0, 256])
#
# plt.title('Color Distribution for All Images')
# plt.xlabel('Color Intensity')
# plt.ylabel('Density')
# plt.legend(['Blue', 'Green', 'Red'])
# plt.show()

gt = cv2.imread("../dataset/train/masks/bottom_left.png")
pred = cv2.imread("../dataset/train/predictions/bottom_left.png")

and_mask = cv2.bitwise_and(gt, pred) #tp

neg_and = cv2.bitwise_and(cv2.bitwise_not(gt), pred) #fp
neg_or = cv2.bitwise_not(cv2.bitwise_or(cv2.bitwise_not(gt), pred)) #fn
cv2.imshow("and", neg_or)
cv2.waitKey()
