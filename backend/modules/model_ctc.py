import cv2
import numpy as np
import os
from tensorflow import keras
from flask import jsonify


class ModelCtc:
    def __init__(self):
        self.model = keras.models.load_model('modules/letter_digits_sym')

    def preprocess(self, directory):
        temp_list = []
        temp_directory_list = os.listdir(directory)
        for _ in temp_directory_list:
            img = cv2.imread(os.path.join(directory, _), 0)
            pad = []
            for x in img.shape:
                while True:
                    if x % 28 == 0:
                        pad.append(x)
                        break
                    else:
                        x += 1
            ratio = int(pad[0]/pad[1])
            img = cv2.copyMakeBorder(img, int(pad[0]/2), int(pad[0]/2),
                                     int(pad[1]/2)*ratio, int(pad[1]/2)*ratio, cv2.BORDER_CONSTANT)
            img = cv2.resize(img, (408, 408))
            img = cv2.resize(img, (204, 204))
            img = cv2.resize(img, (102, 102))
            img = cv2.resize(img, (56, 56))
            img = cv2.resize(img, (28, 28))
            img = img.reshape((28, 28, 1))
            temp_list.append(img)
        return np.array(temp_list)

    def predict_ctc(self, data):
        dict = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h", 8: "i", 9: "j", 10: "k", 11: "l",
                12: "m", 13: "n", 14: "o", 15: "p", 16: "q", 17: "r", 18: "s", 19: "t", 20: "u", 21: "v", 22: "w",
                23: "x", 24: "y", 25: "z", 26: "0", 27: "1", 28: "2", 29: "3", 30: "4", 31: "5", 32: "6", 33: "7",
                34: "8", 35: "9", 36: "!", 37: "(", 38: ")", 39: "+", 40: ",", 41: "-"}
        resp = self.model.predict(data)
        resp = [dict[np.argmax(_)] for _ in resp]
        return jsonify({"data": resp, "status": '200'})