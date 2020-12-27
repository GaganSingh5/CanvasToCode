import cv2
import numpy as np
import os
import shutil


def preprocess_image_split(image):
    try:
        os.mkdir('temp')
    except:
        shutil.rmtree('temp')
        os.mkdir('temp')
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img[np.where(img > 230)] = 0
    thresh = cv2.threshold(img, 0, 200, cv2.THRESH_BINARY)[1]
    result = img.copy()
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    count = 10
    path = 'temp'
    for cntr in contours:
        x, y, w, h = cv2.boundingRect(cntr)
        cv2.rectangle(result, (x, y), (x+w, y+h), (255, 0, 0), 2)
        crop_img = img[y:y + h, x:x + w]
        cv2.imwrite(os.path.join(path, "{}.jpg".format(count)), crop_img)
        count += 1
    return {"path": path, "status": 200}
