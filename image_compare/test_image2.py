from PIL import Image
import imagehash

def calculate_similarity(image_path1, image_path2):
    try:
        # Open and load the images
        img1 = Image.open(image_path1)
        img2 = Image.open(image_path2)

        # Compute the perceptual hash of the images
        hash1 = imagehash.average_hash(img1)
        hash2 = imagehash.average_hash(img2)

        # Calculate the hamming distance between the hashes
        # The Hamming distance is a measure of the number of differing bits between two strings.
        # A lower Hamming distance implies a higher similarity.
        hamming_distance = hash1 - hash2

        return hamming_distance

    except OSError as e:
        print(f"Error: {e}")
        return None

# Example usage:
image_path1 = "MonaLisa_1.jpg"
image_path2 = "Other.jpg"

similarity = calculate_similarity(image_path1, image_path2)

if similarity is not None:
    print(f"Hamming distance (image similarity): {similarity}")
else:
    print("Error calculating similarity.")
