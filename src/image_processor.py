import torch
import numpy as np
from cryptography.fernet import Fernet
import logging

class ImageProcessor:  
    def __init__(self):
        self.key = None
        self.cipher_suite = None

    def generate_key(self):
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        return self.key

    def set_key(self, key):
        key_bytes = bytes(key[2:-1], 'utf-8')
        self.key = key_bytes
        self.cipher_suite = Fernet(self.key)



    def encrypt_data(self, data):
        data_shape = data.shape
        return self.cipher_suite.encrypt(data.tobytes()), data_shape

    def decrypt_data(self, encrypted_data, original_shape):
        decrypted_data = self.cipher_suite.decrypt(encrypted_data)
        return np.frombuffer(decrypted_data, dtype=np.uint8).reshape(original_shape)

    def prepare_image(self, image: np.ndarray, x: int, y: int, width: int, height: int, size: int):
        if len(image.shape) != 3 or image.shape[2] != 3:
            raise ValueError("Image should have 3 dimensions and a shape of (height, width, 3)")

        if width < 2 or height < 2 or size < 2:
            raise ValueError("Width, height, and size must be greater than or equal to 2")

        if x < 0 or x + width > image.shape[1]:
            raise ValueError(f"Invalid x-coordinate. x should be in the range [0, {image.shape[1] - width}]")

        if y < 0 or y + height > image.shape[0]:
            raise ValueError(f"Invalid y-coordinate. y should be in the range [0, {image.shape[0] - height}]")

        pixelated_image = image.copy()
        pixelated_area = pixelated_image[y:y + height, x:x + width]

        # Encrypt the original pixel data before pixelating
        target_array = image[y:y + height, x:x + width]

        for h in range(0, height, size):
            for w in range(0, width, size):
                mean = np.mean(pixelated_area[h: h + size, w: w + size], axis=(0, 1))
                pixelated_area[h: h + size, w: w + size] = mean

        pixelated_image[y:y + height, x:x + width] = pixelated_area


        return pixelated_image, target_array

    