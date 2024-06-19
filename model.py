from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import os
import logging

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('tensorflow').setLevel(logging.ERROR)

class ImageClassifier:
    def __init__(self, model_path, labels_path):
        self.model = load_model(model_path, compile=False)
        self.class_names = open(labels_path, "r").readlines()
        self.input_size = (224, 224)

    def preprocess_image(self, image_path):
        image = Image.open(image_path).convert("RGB")
        image = ImageOps.fit(image, self.input_size, Image.Resampling.LANCZOS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        data[0] = normalized_image_array
        return data

    def predict(self, image_path):
        data = self.preprocess_image(image_path)
        prediction = self.model.predict(data)
        index = np.argmax(prediction)
        class_name = self.class_names[index]
        confidence_score = prediction[0][index]
        return class_name, confidence_score



