import cv2
from src.face_detector import FaceDetector
from src.image_processor import ImageProcessor
from PIL import Image
import pickle
import numpy as np
import os
import logging

class ImagePixelizer:
    def __init__(self):
        self.detector = FaceDetector()
        self.processor = ImageProcessor()  # Assuming ImageProcessor class is defined with necessary methods

    def load_image(self, img_path):
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError(f"Could not open or find the image: {img_path}")
        return img

    def process_faces(self, img, img_path, encrypt_path="output/encrypted_data/encrypted_img.pkl"):

        details_list = []

        detected_faces = self.detector.detect_faces(img_path)
        pixelated_image = img.copy()
        
        for face in detected_faces:
            x, y, w, h = face
            pixel_size = int((w+h) / 2 / 4)
            pixelated_image, non_pixelated_target = self.processor.prepare_image(pixelated_image, x, y, w, h, pixel_size)
            encrypted_non_pixelated_target, data_shape = self.processor.encrypt_data(non_pixelated_target)

            details = {
                "encrypted_data": encrypted_non_pixelated_target,
                "original_shape": data_shape,
                "coords": (x, y, w, h)
            }
            details_list.append(details)

            os.makedirs(os.path.dirname(encrypt_path), exist_ok=True)
            with open(encrypt_path, "wb") as file:
                pickle.dump(details_list, file)

        return pixelated_image

    def save_image(self, img, output_path):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img.astype('uint8'))
        img_pil.save(output_path)

    def pixelize_image(self, img_path, output_path):
        img_path = str(img_path)
        img = self.load_image(img_path)
        self.processor.generate_key()
        pixelated_image = self.process_faces(img, img_path)
        self.save_image(pixelated_image, output_path)
        logging.info(f"Generated key: {self.processor.key}")
        return self.processor.key

    def depixelize_image(self, img_path, output_path, encryption_key, encrypted_data_path=os.path.join("output", "encrypted_data", "encrypted_img.pkl")): #save it with the actualfilename
        img_path = str(img_path)
        img = self.load_image(img_path)

        self.processor.set_key(encryption_key)

        with open(encrypted_data_path, "rb") as file:
            details_list = pickle.load(file)

        for details in details_list:
            encrypted_data = details["encrypted_data"]
            original_shape = details["original_shape"]
            x, y, w, h = details["coords"]
            decrypted_data = self.processor.decrypt_data(encrypted_data, original_shape)
            img[y:y+h, x:x+w] = decrypted_data

        self.save_image(img, output_path)



if __name__ == "__main__":
    img_path = "C:/Users/armil/Pictures/Dolomitas/IMG_0027.JPG"
    output_path = "output\pixelated_images/pixelated.jpg"

    pixelizer = ImagePixelizer()
    pixelizer.pixelize_image(img_path, output_path)