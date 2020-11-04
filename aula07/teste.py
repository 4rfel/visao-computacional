import G6_iris_recognition

G6_iris_recognition.iris_model_train("images_new/", "model.pickle")

iris_name = G6_iris_recognition.iris_model_test("model.pickle", "images/0000/0000_000.bmp")
print(iris_name)