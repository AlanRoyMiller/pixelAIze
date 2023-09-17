import cv2

class FaceDetector:
    def __init__(self):
        # Load pre-trained face detection model (you might need to adjust the path)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def detect_faces(self, image_path):
        """
        Detect faces in an image.

        Parameters:
        image_path (str): The path to the image file.

        Returns:
        list: A list of tuples containing the coordinates of the bounding boxes of detected faces.
        """
        # Read the image
        image = cv2.imread(image_path)
        
        if image is None:
            raise ValueError(f"Could not open or find the image: {image_path}")

        # Convert the image to gray scale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  
        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(40, 40))

        return faces

    def draw_faces(self, image_path, output_path):
        """
        Draw bounding boxes around detected faces in an image and save the result.

        Parameters:
        image_path (str): The path to the image file.
        output_path (str): The path to save the output image.

        Returns:
        None
        """
        # Read the image
        image = cv2.imread(image_path)
        
        if image is None:
            raise ValueError(f"Could not open or find the image: {image_path}")

        # Detect faces
        faces = self.detect_faces(image_path)

        # Draw bounding boxes around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Save the result
        cv2.imwrite(output_path, image)

# Example usage
if __name__ == "__main__":
    detector = FaceDetector()
    detector.draw_faces("C:/Users/armil/Pictures/Dolomitas/IMG_9834.JPG", 'output/pixelated_images/output.jpg')
