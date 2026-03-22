import cv2

class ImageProcessingService:
    
    @staticmethod
    def to_grayscale(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return gray