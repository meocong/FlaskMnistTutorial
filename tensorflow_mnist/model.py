import os 
import tensorflow as tf
import numpy as np 
import cv2 

class Tf_Mnist:
    def __init__(self, model_path):
        with tf.gfile.GFile(model_path, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())

        with tf.Graph().as_default() as graph:
            tf.import_graph_def(graph_def, name='conv2d')
        
        self.graph = graph

        self.X = graph.get_tensor_by_name('conv2d/input/X:0')
        self.output = graph.get_tensor_by_name('conv2d/output/predict:0')

        self.sess = tf.Session(graph=self.graph)

    def predict(self, X):
        pd = self.sess.run(self.output, feed_dict={self.X: X})

        return pd

    def predict_image(self, image):
        if len(image.shape) == 3 and image.shape[2] != 1:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        infer_image = np.reshape(image, (1, 28, 28, 1))

        return self.predict(infer_image)

if __name__ == '__main__':
    import glob 

    data_images = glob.glob("../data/mnist/*.jpg")
    model = Tf_Mnist("../data/weights/tf.pb")
    
    for image_path in data_images[:5]:
        image = cv2.imread(image_path, 0)

        predicted = model.predict_image(infer_image)
        print("Predicted for image {0} is {1}".format(image_path.split("/")[-1], np.argmax(predicted)))

        cv2.imshow("image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows

