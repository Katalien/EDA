import os

class FileIterator:

    @staticmethod
    def get_images_from_lowest_level_folders(directory):
        image_files = []
        deepest_directories = []

        for root, dirs, files in os.walk(directory):
            if not dirs:  # Проверяем, есть ли поддиректории
                current_images = []
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.isfile(file_path):
                        current_images.append(file_path)
                if current_images:
                    image_files.extend(current_images)
                    deepest_directories.append(root)

        return image_files, deepest_directories

    @staticmethod
    def get_origin_image(dir):
        pass



#
# # Пример использования
# directory = "../dataset/real_dataset/"
#
# image_files, deepest_directories = FileIterator.get_images_from_lowest_level_folders(directory)
#
# for i, dir_path in enumerate(deepest_directories):
#     print()
#     print(f"Directory: {dir_path}")
#     print("Images:")
#     for image_file in image_files:
#         if os.path.dirname(image_file) == dir_path:
#             print(f"  {image_file}")