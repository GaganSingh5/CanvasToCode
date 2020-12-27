from flask import Flask, request
from PIL import Image
import numpy as np
from modules.general import preprocess_image_split
from modules.model_ctc import ModelCtc
import shutil
codeToCanvas = Flask(__name__)
model = ModelCtc()


@codeToCanvas.route('/', methods=['POST'])
def default():
    image = request.files['image']
    image_read = Image.open(image.stream)
    del image
    img = np.array(image_read)
    del image_read
    path = preprocess_image_split(img)
    del img
    data = model.preprocess(path['path'])
    shutil.rmtree(path['path'])
    del path
    pred = model.predict_ctc(data)
    return pred


if __name__ == '__main__':
    codeToCanvas.run()
