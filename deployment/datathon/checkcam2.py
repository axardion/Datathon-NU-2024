import cv2
import matplotlib.pyplot as plt
import numpy as np
from paddleocr import PaddleOCR, draw_ocr

# Initialize the PaddleOCR reader (supports English)
ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Initialize PaddleOCR

# Load the image using OpenCV
image_path = 'media/photo_AIabg8z.jpg'  # Replace with your image path
image = cv2.imread(image_path)

# 1. Resize the image using OpenCV (scale up by 2x)
scale_percent = 200  # Scale by 200%
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)
resized_img = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)

# 2. Convert to grayscale using OpenCV
gray_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)

# 3. Apply thresholding to make the image binary (black and white)
_, threshold_img = cv2.threshold(gray_img, 128, 255, cv2.THRESH_BINARY)
inverted_img = cv2.bitwise_not(threshold_img)

# Display the preprocessed image (for debugging)
cv2.imshow('Preprocessed Image', inverted_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Use PaddleOCR to detect text in the processed image
results = ocr.ocr(inverted_img)

# Filter to keep only numbers
numbers = []
for result in results:
    for line in result:
        text = line[1][0]  # Extract the detected text
        if text.replace('.', '', 1).isdigit():  # Only keep numbers (including floats)
            numbers.append(text)

# Print the recognized numbers
print("Recognized numbers:", numbers)
float_sum = sum(float(num) for num in numbers if '.' in num)
print("Sum of area:", float_sum)
# Optionally, display the image with bounding boxes around recognized numbers
boxes = [line[0] for result in results for line in result if line[1][0].replace('.', '', 1).isdigit()]
if boxes:
    # Convert boxes to the required format for drawing
    for box in boxes:
        top_left = tuple(map(int, box[0]))
        bottom_right = tuple(map(int, box[2]))
        inverted_img = cv2.rectangle(inverted_img, top_left, bottom_right, (0, 255, 0), 2)

# Show the result image with bounding boxes
plt.imshow(inverted_img, cmap='gray')
plt.axis('off')
plt.show()
