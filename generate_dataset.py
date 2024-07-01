import cv2
import numpy as np
import os


def generate_test_data(filepath, n, image_size=(640, 480), mask_white_areas=5):
    os.makedirs(filepath, exist_ok=True)
    gray_value=128

    for i in range(n):
        folder_name = f"{i + 1:02d}"
        folder_path = os.path.join(filepath, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        # Generate a random grayscale image
        image = np.full(image_size, gray_value, dtype=np.uint8)

        # Generate a random binary mask
        mask = np.zeros(image_size, dtype=np.uint8)

        for _ in range(mask_white_areas):
            x, y = np.random.randint(0, image_size[1]), np.random.randint(0, image_size[0])
            width, height = np.random.randint(10, 100), np.random.randint(10, 100)
            cv2.rectangle(mask, (x, y), (x + width, y + height), 255, -1)

        # Save the image and the mask
        image_path = os.path.join(folder_path, f"{folder_name}.png")
        mask_path = os.path.join(folder_path, f"{folder_name}_mask.png")

        cv2.imwrite(image_path, image)
        cv2.imwrite(mask_path, mask)


# Example usage
generate_test_data("../dataset/test_data/", 10)