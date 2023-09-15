import cv2

class Pixelizer:
    def __init__(self):
        pass

    @staticmethod
    def pixelate_region(image, x, y, w, h, pixel_size=500):
        """
        Pixelates a region within an image.

        Parameters:
        image (numpy.ndarray): The input image.
        x (int): The x-coordinate of the top-left corner of the region to pixelate.
        y (int): The y-coordinate of the top-left corner of the region to pixelate.
        w (int): The width of the region to pixelate.
        h (int): The height of the region to pixelate.
        pixel_size (int): The size of the squares to use for pixelation. Larger values will result in more pixelation.

        Returns:
        numpy.ndarray: The image with the specified region pixelated.
        """
        # Crop the region to be pixelated
        region = image[y:y+h, x:x+w]
        
        # Downscale the region to reduce the number of pixels, then upscale it back to the original size
        region = cv2.resize(region, (w // pixel_size, h // pixel_size), interpolation=cv2.INTER_LINEAR)
        region = cv2.resize(region, (w, h), interpolation=cv2.INTER_NEAREST)
        
        # Replace the original region with the pixelated region
        image[y:y+h, x:x+w] = region

        return image

    def pixelate_faces(self, image_path, output_path, faces, pixel_size=10):
        """
        Pixelates the faces in an image and saves the result.

        Parameters:
        image_path (str): The path to the image file.
        output_path (str): The path to save the output image.
        faces (list): A list of tuples containing the coordinates of the bounding boxes of the faces.
        pixel_size (int): The size of the squares to use for pixelation.

        Returns:
        None
        """
        # Read the image
        image = cv2.imread(image_path)
        
        if image is None:
            raise ValueError(f"Could not open or find the image: {image_path}")

        # Pixelate each face in the image
        for (x, y, w, h) in faces:
            image = self.pixelate_region(image, x, y, w, h, pixel_size)

        # Save the result
        cv2.imwrite(output_path, image)

# Example usage
if __name__ == "__main__":
    from face_detector_module import FaceDetector

    # Initialize the face detector and pixelizer
    detector = FaceDetector()
    pixelizer = Pixelizer()

    # Define the paths
    image_path = "C:/Users/armil/Pictures/Dolomitas/IMG_9834.JPG" 
    output_path = "output/pixelated_images/output_pixelize.jpg"

    # Detect faces and pixelate them
    faces = detector.detect_faces(image_path)
    pixelizer.pixelate_faces(image_path, output_path, faces, pixel_size=10)
