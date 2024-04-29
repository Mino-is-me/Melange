import os
from PIL import Image

target_drive = 'E:/wip/'
folder_path = target_drive + 'CINEVStudio/'

for root, dirs, files in os.walk(folder_path):
    for filename in files:
        print(filename)
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.tga'):
            image_path = os.path.join(root, filename)
            image = Image.open(image_path)
            width, height = image.size
            new_width = 2048
            new_height = int(height * new_width / width)
            resized_image = image.resize((new_width, new_height))
            resized_image.save(image_path)
print("All images resized successfully.")