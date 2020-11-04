import G6_iris_recognition as iris
from time import time

with open("model.pickle", "wb") as model:
    pass

t0 = time()
iris.iris_model_train("treated_images", "model.pickle")
t1 = round((time() - t0) / 60, 2)

print(f"time elapsed: {t1}m")