import cv2
from src.face_detector import FaceDetector
from src.image_processor import ImageProcessor
from PIL import Image

class ImagePixelizer:
    def __init__(self):
        self.detector = FaceDetector()
        self.processor = ImageProcessor()  # Assuming ImageProcessor class is defined with necessary methods

    def load_image(self, img_path):
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError(f"Could not open or find the image: {img_path}")
        return img

    def process_faces(self, img, img_path):
        detected_faces = self.detector.detect_faces(img_path)
        final_img = img.copy()
        
        for face in detected_faces:
            x, y, w, h = face
            pixel_size = int((w+h) / 2 / 4)
            final_img, _, _ = self.processor.prepare_image(final_img, x, y, w, h, pixel_size)
        
        return final_img

    def save_image(self, img, output_path):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img.astype('uint8'))
        img_pil.save(output_path)

    def pixelize_image(self, img_path, output_path):
        img_path = str(img_path)
        img = self.load_image(img_path)
        final_img = self.process_faces(img, img_path)
        self.save_image(final_img, output_path)

if __name__ == "__main__":
    img_path = "C:/Users/armil/Pictures/Dolomitas/IMG_0027.JPG"
    output_path = "output\pixelated_images/pixelated.jpg"

    pixelizer = ImagePixelizer()
    pixelizer.pixelize_image(img_path, output_path)