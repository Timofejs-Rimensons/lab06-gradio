import cv2
import numpy as np
import torch
from torchvision import transforms
from efficientnet_pytorch import EfficientNet
from torchvision.models import EfficientNet_B0_Weights

class ImageProcessingService:
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((224, 224)),
        transforms.Normalize(
            [0.485, 0.456, 0.406],
            [0.229, 0.224, 0.225])
    ])
    
    model = EfficientNet.from_pretrained('efficientnet-b0')
    model.eval()
    
    weights = EfficientNet_B0_Weights.DEFAULT
    categories = weights.meta["categories"]
    
    @staticmethod
    def to_grayscale(img_array):
        gray_img = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
        return gray_img, "Image successfully turned into grayscale version"
    
    @staticmethod
    def extract_details(img_array):
        kernel = np.array([
            [1, 0, -1],
            [2, 0, -2],
            [1, 0, -1]
        ], dtype=np.float32)
        
        detailed_img = cv2.filter2D(img_array, -1, kernel)
        return detailed_img, "Kernel is successfully applied on the image"
        
    @classmethod
    def label_object(cls, img_array):
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize((224, 224)),
            transforms.Normalize(
                [0.485, 0.456, 0.406],
                [0.229, 0.224, 0.225])
        ])
        
        img_tensor = cls.transform(img_array).unsqueeze(0)
        with torch.no_grad():
            output = cls.model(img_tensor)
            
        probabilities = torch.softmax(output, dim=1)
        predicted_idx = probabilities.argmax(dim=1).item()
        
        predicted_label = cls.categories[predicted_idx]
        confidence = probabilities[0, predicted_idx].item()
            
        return img_array, f"Object Label: '{predicted_label}' {round(confidence*100, 2)}%"
    
    @staticmethod
    def to_black_and_white(img_array):
        if img_array.ndim == 3:
            img_array = np.mean(img_array, axis=2)

        shape = img_array.shape

        f = np.fft.fftfreq(shape[0])[:, None]
        g = np.fft.fftfreq(shape[1])[None, :]
        freq = np.sqrt(f**2 + g**2)
        freq[0, 0] = 1

        white = np.fft.fft2(np.random.randn(*shape))
        blue = white * freq

        blue = np.fft.ifft2(blue).real
        blue_thresholds = (blue - blue.min()) / (blue.max() - blue.min())

        img_array = img_array / 255
        binary_img = (img_array > blue_thresholds).astype(int)
        binary_img = binary_img * 255

        return binary_img, "Image successfully turned into B&W version"