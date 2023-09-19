import cv2

class FaceDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def detect_faces(self, image_path):
        image = cv2.imread(image_path)
        
        if image is None:
            raise ValueError(f"Could not open or find the image: {image_path}")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

        return faces


    def draw_faces(self, image_path, output_path):
        image = cv2.imread(image_path)
        
        if image is None:
            raise ValueError(f"Could not open or find the image: {image_path}")

        faces = self.detect_faces(image_path)

        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imwrite(output_path, image)


if __name__ == "__main__":
    detector = FaceDetector()
    detector.draw_faces("C:/Users/armil/Pictures/Dolomitas/IMG_9834.JPG", 'output/pixelated_images/output.jpg')
