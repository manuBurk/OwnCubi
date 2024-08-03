import cv2
import numpy as np

def compare_images(image1_path, image2_path):
    # Load the two images
    image1 = cv2.imread(image1_path, cv2.IMREAD_COLOR)
    image2 = cv2.imread(image2_path, cv2.IMREAD_COLOR)

    # Check if the images were loaded properly
    if image1 is None or image2 is None:
        return False, "One or both images could not be loaded"

    # Check if the images have the same shape
    if image1.shape != image2.shape:
        return False, f"Images have different shapes: {image1.shape} vs {image2.shape}"

    # Method 1: Pixel-wise comparison
    if np.array_equal(image1, image2):
        return True, "Images are exactly the same"

    # Method 2: Histogram comparison
    hist1 = cv2.calcHist([image1], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
    hist2 = cv2.calcHist([image2], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
    hist1 = cv2.normalize(hist1, hist1).flatten()
    hist2 = cv2.normalize(hist2, hist2).flatten()
    hist_comparison = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    if hist_comparison == 1:
        return True, "Images are the same based on histogram comparison"
    else:
        return False, f"Histogram comparison score: {hist_comparison}"


   
# Example usage
image1_path = "/nethome/lkiefer/pogo/CubiCasa5k/data/cubicasa5k/high_quality_architectural/551/F1_original.png"
image2_path = "/nethome/lkiefer/pogo/CubiCasa5k/data/cubicasa5k/high_quality_architectural/551/F1_scaled.png"
result, message = compare_images(image1_path, image2_path)
print(message)
