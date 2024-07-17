# from image_match.goldberg import ImageSignature
# gis = ImageSignature()
# a = gis.generate_signature('./MonaLisa_1.jpg');
# b = gis.generate_signature('./MonaLisa_2.jpg');
# c = gis.generate_signature('./Other.jpg');
# dist = gis.normalized_distance(a,b)
# dist2 = gis.normalized_distance(a,c);
# # normalized distance < 0.4 likely to be a match
# print(dist)
# print(dist2)

import numpy as np
import cv2

def mse(imageA, imageB):
    # Mean Squared Error between two images is the sum of the squared difference between the two images
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

def psnr(imageA, imageB):
    # Peak Signal to Noise Ratio between two images
    mse_value = mse(imageA, imageB)
    if mse_value == 0:
        return 100
    PIXEL_MAX = 255.0
    return 20 * np.log10(PIXEL_MAX / np.sqrt(mse_value))

# Example usage:
path_to_image1 = "MonaLisa_1.jpg"
path_to_image2 = "Other.jpg"

image1 = cv2.imread(path_to_image1)
image2 = cv2.imread(path_to_image2)

# Resize the images to the same dimensions
dim = (1024, 687) # You can change this to the desired dimensions
image1 = cv2.resize(image1, dim, interpolation = cv2.INTER_AREA)
image2 = cv2.resize(image2, dim, interpolation = cv2.INTER_AREA)

if image1 is not None and image2 is not None:
    print(f"MSE between the images: {mse(image1, image2)}")
    print(f"PSNR between the images: {psnr(image1, image2)}")
else:
    print("Error: One or both images could not be loaded.")