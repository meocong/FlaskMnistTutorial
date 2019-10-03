from flask import Flask, request, render_template, jsonify
from tensorflow_mnist.model import Tf_Mnist
import time 
from io import BytesIO
import base64
import numpy as np
from PIL import Image
import cv2 
from flask_cors import CORS

tf_mnist_model = Tf_Mnist("./data/weights/tf.pb")
app = Flask(__name__)
CORS(app)

def read_image(img_bytes):
    # if (img_bytes is np.array):
    #     return img_bytes
    return cv2.imdecode(np.asarray(bytearray(img_bytes.read()), dtype="uint8"), cv2.IMREAD_COLOR)


# Testing URL
@app.route('/hello/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello, World!'

#Tensorflow MNIST
@app.route('/tf', methods=['POST'])
def tf_predict():
    # initialize the data dictionary that will be returned from the
    start_time = time.time()
    data = {"success": False}

    if request.method == "POST":
        image = request.files.get("image", None)
        if image is not None:
            try:
                # Read image by Opencv
                image = read_image(image)

                # classify the input image
                temp = tf_mnist_model.predict_image(image)

                data["output"] = int(np.argmax(temp))
                data["confidence"] = float(np.max(temp))
                # indicate that the request was a success
                data["success"] = True
            except Exception as ex:
                data['error'] = ex
                print(str(ex))
        else:
            image = request.form.get("image", None)

            if image is not None:
                try: 
                    # Read Image 
                    image = image.split("base64,")[1]
                    image = BytesIO(base64.b64decode(image))
                    image = Image.open(image) 
                    image = Image.composite(image, Image.new('RGB', image.size, 'white'), image)
                    image = image.convert('L')
                    image = image.resize((28, 28), Image.ANTIALIAS) 
                    image = 1 - np.array(image, dtype=np.float32) / 255.0

                    # classify the input image
                    temp = tf_mnist_model.predict_image(image)

                    data["output"] = int(np.argmax(temp))
                    data["confidence"] = float(np.max(temp))
                    # indicate that the request was a success
                    data["success"] = True
                except Exception as ex:
                    data['error'] = ex
                    print(str(ex))

    data['run_time'] = "%.2f" % (time.time() - start_time)
    # return the data dictionary as a JSON response
    return jsonify(data)

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=3000)




