from typing import Dict, List
from FeatureAnalysis import FeatureSummary
import cv2
import os
import matplotlib.pyplot as plt
import re
from psd_tools import PSDImage
import numpy as np



def buildFeatures(features_config: Dict[str, List]) -> Dict[str, List]:
    features2analyze = {}
    for key, val in features_config.items():
        capitalKey = key.capitalize() + "Analysis"
        features2analyze[capitalKey] = list(val)
    return features2analyze

# def parse_image_path( path):
#     dir_path = os.path.dirname(path)
#     filename = os.path.basename(path)
#     filename_no_ext, file_extension = os.path.splitext(filename)
#     match = re.match(r'(\d+)_([a-z]+)', filename_no_ext)
#     if match:
#         image_number = match.group(1)
#         class_type = match.group(2)
#         return dir_path, image_number, class_type, file_extension
#     else:
#         raise ValueError("Неверный формат имени файла")

# def mask_path2image_path(mask_path):
#     dir_path, image_number, class_type, file_ext = parse_image_path(mask_path)
#     possible_extensions = [".tif", ".tiff", ".png", ".jpg"]
#
#     for ext in possible_extensions:
#         image_path = f"{dir_path}/{image_number}{ext}"
#         if os.path.exists(image_path):
#             return image_path

def sort_general_custom_features(featureSummaries: FeatureSummary):
    general, custom = [], []
    for feature in featureSummaries:
        if feature.features_list[0].class_name == "General":
            general.append(feature)
        else:
            custom.append(feature)
    return general, custom

def show_plots( images, titles=None, bgr2rgb=True):
    cols = len(images)
    new_images = []
    if titles is None:
        titles = []
        for i in range(len(images)):
            titles.append("")
    if bgr2rgb:
        for image in images:
            new_images.append(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        images = new_images
    for i, image_title in enumerate(zip(images, titles)):
        image = image_title[0]
        title = image_title[1]
        plt.subplot(1, cols, i + 1)  # 1 строка, 2 столбца, позиция 1
        plt.imshow(image)
        plt.axis('off')
        plt.title(title)

    plt.show()

def show_image( image, name="show"):
    image_min = cv2.resize(image, (0, 0), fx=0.4, fy=0.4)
    cv2.imshow(name, image_min)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_plt(image, title="image", bgr2rgb=False, bgr2gray=False):
    if bgr2rgb:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    if bgr2gray:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    plt.imshow(image)
    plt.axis('off')
    plt.title(title)
    plt.show()


def parse_mask_path( path):
    dir_path = os.path.dirname(path)
    filename = os.path.basename(path)
    filename_no_ext, file_extension = os.path.splitext(filename)
    match = re.match(r'(\d+)_([a-z]+)', filename_no_ext)
    if match:
        image_number = match.group(1)
        class_type = match.group(2)
        return dir_path, image_number, class_type, file_extension
    else:
        raise ValueError("Неверный формат имени файла")

def mask_path2image_path(mask_path):
    print(mask_path)
    dir_path, image_number, class_type, file_ext = parse_mask_path(mask_path)
    possible_extensions = [".tif", ".tiff", ".png", ".jpg", ".psd"]

    for ext in possible_extensions:
        image_path = f"{dir_path}/{image_number}{ext}"
        if os.path.exists(image_path):
            print(image_path)
            return image_path


def parse_image_path(path):
    # Получаем директорию и имя файла
    dir_path = os.path.dirname(path)
    filename = os.path.basename(path)

    # Разделяем имя файла и расширение
    filename_no_ext, file_extension = os.path.splitext(filename)

    # Ищем число в имени файла
    match = re.match(r'(\d+)', filename_no_ext)
    if match:
        image_number = match.group(1)

        # Формируем имя файла маски
        mask_filename = f"{image_number}_sco.tif"

        # Получаем полный путь к файлу маски
        mask_path = os.path.join(dir_path, mask_filename)

        if not os.path.exists(mask_path):
            mask_path = f"{image_number}_sco.tiff"


        return mask_path
    else:
        raise ValueError("Неверный формат имени файла")

def image_path2mask_path(image_path):
    return parse_image_path(image_path)


def get_np_from_psd(image_path):
    psd = PSDImage.open(image_path)
    layers = psd._layers
    for i, layer in enumerate(layers):
        image = layer.topil()
        image_np = np.array(image)
        if image_np.shape[2] == 3:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        return image_np

