import os
from PIL import Image, ImageDraw

# Создание папки для хранения изображений, если она не существует
filepath = '../dataset/train/predictions/'
os.makedirs(filepath, exist_ok=True)

# Размеры изображений
image_size = (200, 200)
square_size = (50, 50)
offset = 10

# Позиции для белых квадратов с отступами
positions = [
    (offset, offset),  # Левый верхний угол
    (image_size[0] - square_size[0] - offset, offset),  # Правый верхний угол
    (offset, image_size[1] - square_size[1] - offset),  # Левый нижний угол
    (image_size[0] - square_size[0] - offset, image_size[1] - square_size[1] - offset)  # Правый нижний угол
]
filenames = ['top_left.png', 'top_right.png', 'bottom_left.png', 'bottom_right.png']

for position, filename in zip(positions, filenames):
    # Создание черного изображения
    image = Image.new("RGB", image_size, "black")
    draw = ImageDraw.Draw(image)

    # Определение координат белого квадрата
    x0, y0 = position
    x1, y1 = (x0 + square_size[0], y0 + square_size[1])

    # Рисование белого квадрата
    draw.rectangle([x0, y0, x1, y1], fill="white")

    # Сохранение изображения
    image.save(os.path.join(filepath, filename))

print("Изображения успешно созданы и сохранены.")