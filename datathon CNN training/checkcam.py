import cv2
import numpy as np
import tensorflow as tf

# Load the model
model = tf.keras.models.load_model('model1.h5')

def apply_canny_edge(image):
    # Convert to grayscale and upscale the resolution
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image = cv2.resize(gray_image, (gray_image.shape[1] * 1, gray_image.shape[0] * 1),
                            interpolation=cv2.INTER_CUBIC)
    # Apply Canny edge detection with higher thresholds for clearer edges
    edges = cv2.Canny(gray_image, 30, 40)
    return edges

# Define the categories
categories = ['0', '1', '2']

IMG_WIDTH = 154
IMG_HEIGHT = 116

# Load the image
image_path = '00.jpg'  # Replace with your image file path
image = cv2.imread(image_path)

if image is not None:
    
    # Apply contrast adjustment
    alpha = 3  # Contrast control (>1 increases contrast)
    beta = 0     # Brightness control (optional)
    contrast_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    
    # Apply sharpening filter
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(contrast_image, -1, kernel)
    
    # Apply Canny edge detection
    edge_image = apply_canny_edge(sharpened)

    # Resize for model input
    img = cv2.resize(edge_image, (IMG_WIDTH, IMG_HEIGHT))
    reshaped_img = np.reshape(img, (1, IMG_HEIGHT, IMG_WIDTH, 1))
    
    # Show intermediate result
    cv2.imshow('Processed Image', img)
    cv2.waitKey(0)

    # Make prediction
    prediction = model.predict(reshaped_img)
    category_index = np.argmax(prediction)
    category = categories[category_index]
    confidence = prediction[0][category_index]
    
    # Print debug information
    print(f"Raw prediction: {prediction}")
    print(f"Predicted category: {category}")
    print(f"Confidence: {confidence:.2f}")
    
    # Put text on the original image
    text = f"{category}: {confidence:.2f}"
    cv2.putText(image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Display the final result
    cv2.imshow('Mask Detection', image)
    cv2.waitKey(0)  # Wait for a key press to close the image window

    # Close all windows
    cv2.destroyAllWindows()
else:
    print(f"Error: Image at path '{image_path}' could not be loaded.")
