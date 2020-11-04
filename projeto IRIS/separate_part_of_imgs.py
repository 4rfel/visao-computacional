import os
import cv2
import shutil
from time import sleep

shutil.rmtree("part_images", ignore_errors=True)
sleep(1)
os.mkdir("part_images")

# folders = [0, 2, 3, 9]
folders = range(60)

img_dir = "images"

for i in folders:
    dir_name = str(i).zfill(4)
    if not os.path.isdir(f"part_images/{dir_name}"):
        os.mkdir(f"part_images/{dir_name}")
    for j in range(20):
        img_path = f"{dir_name}/{dir_name}_{str(j).zfill(3)}.bmp"
        img = cv2.imread(f"{img_dir}/{img_path}")
        cv2.imwrite(f"part_images/{img_path}", img)