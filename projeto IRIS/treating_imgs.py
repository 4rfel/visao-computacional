import cv2
import numpy as np
import os
from time import time, sleep
import shutil

def unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
	"""Return a sharpened version of the image, using an unsharp mask."""
	blurred = cv2.GaussianBlur(image, kernel_size, sigma)
	sharpened = float(amount + 1) * image - float(amount) * blurred
	sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
	sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
	sharpened = sharpened.round().astype(np.uint8)
	if threshold > 0:
		low_contrast_mask = np.absolute(image - blurred) < threshold
		np.copyto(sharpened, image, where=low_contrast_mask)
	return sharpened

def increase_brightness(img, value=30):
	hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
	h, s, v = cv2.split(hsv)

	lim = 255 - value
	v[v > lim] = 255
	v[v <= lim] += value

	final_hsv = cv2.merge((h, s, v))
	img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2RGB)
	return img

def increase_contrast(img, f):
	
	alpha_c = f
	gamma_c = 127*(1-f)

	img = cv2.addWeighted(img, alpha_c, img, 0, gamma_c)
	return img

def cropROI(img, template):

	imgC = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

	template = cv2.GaussianBlur(template, (7, 7), 0)

	width,height=template.shape

	match = cv2.matchTemplate(imgC, template, cv2.TM_CCOEFF_NORMED)

	threshold = 0.6
	position = np.where(match >= threshold)
	last_pos = (0,0)
	iris = False

	for point in zip(*position[::-1]):
		if abs(point[0] - last_pos[0]) < 20 or abs(point[1] - last_pos[1]) < 20:
			continue
		
		y1 = point[1] - 50
		x1 = point[0] - 100
		y2 = point[1] + height + 100
		x2 = point[0] + width + 100

		imgC = imgC[y1:y2, x1:x2]
		last_pos = point
		iris = True
		break

	imgC = cv2.cvtColor(imgC, cv2.COLOR_GRAY2RGB)

	return imgC, iris

"""
TESTS
	- change img type to hsv and increase v value by a fixed amount
	- equalize img histogram (bugs the testing fase)
	- bright img
"""
t0 = time()
shutil.rmtree("treated_images", ignore_errors=True)
sleep(1)
os.mkdir("treated_images")

path = "part_images"
directory_list = list()
for root, dirs, files in os.walk(path, topdown=False):
	for name in dirs:
		directory_list.append(os.path.join(root, name))
directory_size = len(directory_list)

template = cv2.imread("template.png", cv2.IMREAD_GRAYSCALE)


value = 25 # value for increase contrast of img
f = float(131 * (value + 127)) / (127 * (131 - value)) # number that is used in contrast, it is here to minimize computation time
if not os.path.isdir("treated_images"):
	os.mkdir("treated_images")

for i in range(directory_size):
	# print(f"\r{i}/{directory_size}", end="\r")
	dir_name = str(i).zfill(4)
	if not os.path.isdir(f"treated_images/{dir_name}"):
		os.mkdir(f"treated_images/{dir_name}")
	for j in range(20):
		file_name = dir_name + "_" + str(j).zfill(3)
		img = cv2.imread(f"part_images/{dir_name}/{file_name}.bmp")
		img, achou_iris = cropROI(img, template)
		if not achou_iris:
			continue
		img = increase_brightness(img)
		img = unsharp_mask(img)
		img = increase_contrast(img, f)
		cv2.imwrite(f"treated_images/{dir_name}/{file_name}.bmp", img)
	print(f"\r{i+1}/{directory_size}", end="\r")
print(f"time elapsed: {round(time()-t0, 2)}s")