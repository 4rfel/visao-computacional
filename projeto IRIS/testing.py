import G6_iris_recognition as iris
from random import randint
from time import time
import os


images_path = "treated_images"
directory_list = list()
for root, dirs, files in os.walk(images_path, topdown=False):
    for name in dirs:
        directory_list.append(os.path.join(root, name))
directory_size = len(directory_list)

t0 = time()
corrects = 0
unmatchs = 0
total = 0
for i in range(directory_size):
    for root, dirs, files in os.walk(directory_list[i], topdown=False):
        f = files
        total += len(f)
    for j in f:
        guess = iris.iris_model_test("model.pickle", f"treated_images/{str(i).zfill(4)}/{j}")
        if guess == "unmatch":
            unmatchs += 1
        elif int(guess) == i:
            corrects += 1

t1 = round((time() - t0) / 60, 2)

print(f"time elapsed: {t1}min")
print(f"corrects: {corrects}")
print(f"unmatch: {unmatchs}")
print(f"% de acertos: {round(corrects/total*100, 2)}%")