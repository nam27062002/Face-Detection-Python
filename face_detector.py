import cv2
import dlib
import os
import shutil
import numpy as np

class FaceExtractor:
    def __init__(self, cache_dir='Assets/Cache/'):
        self.cache_dir = cache_dir
        self.detector = dlib.get_frontal_face_detector()
        self._clear_cache()

    def _clear_cache(self):
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
        os.makedirs(self.cache_dir)

    def _unsharp_mask(self, image, kernel_size=(5, 5), sigma=1.0, amount=1.5, threshold=0):
        blurred = cv2.GaussianBlur(image, kernel_size, sigma)
        sharpened = float(amount + 1) * image - float(amount) * blurred
        sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
        sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
        sharpened = sharpened.round().astype(np.uint8)

        if threshold > 0:
            low_contrast_mask = np.absolute(image - blurred) < threshold
            np.copyto(sharpened, image, where=low_contrast_mask)

        return sharpened

    def process_images(self, input_dir='Assets/Extract'):
        for filename in os.listdir(input_dir):
            if filename.endswith(".jpg"):
                self._process_single_image(input_dir, filename)

    def _process_single_image(self, input_dir, filename):
        image_path = os.path.join(input_dir, filename)
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray, 1)
        for i, face in enumerate(faces):
            x, y, w, h = (face.left(), face.top(), face.width(), face.height())
            new_x = max(x - w // 2, 0)
            new_y = max(y - h // 2, 0)
            new_w = min(w * 2, image.shape[1] - new_x)
            new_h = min(h * 2, image.shape[0] - new_y)
            face_image_with_border = image[new_y:new_y + new_h, new_x:new_x + new_w]
            sharpened_face = self._unsharp_mask(face_image_with_border)
            face_filename = os.path.join(self.cache_dir, f'{os.path.splitext(filename)[0]}_face_{i + 1}.jpg')
            cv2.imwrite(face_filename, sharpened_face)
            cv2.rectangle(image, (new_x, new_y), (new_x + new_w, new_y + new_h), (255, 0, 0), 2)

