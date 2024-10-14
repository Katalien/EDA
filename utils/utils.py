import cv2
import os
import matplotlib.pyplot as plt
import re
from psd_tools import PSDImage
import numpy as np


def parse_mask_path(path):
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


def get_np_from_psd(image_path):
    psd = PSDImage.open(image_path)
    layers = psd._layers
    for i, layer in enumerate(layers):
        image = layer.topil()
        image_np = np.array(image)
        if image_np.shape[2] == 3:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        return image_np


def show_plots(images, titles=None, bgr2rgb=True):
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


def show_image(image, name="show"):
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
