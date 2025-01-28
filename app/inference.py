import pickle
import cv2
import numpy as np

# Load the trained model
with open('smile_classifier.pkl', 'rb') as f:
    model = pickle.load(f)

# Preprocess the image
def preprocess_image(image):
    image = cv2.resize(image, (64, 64))
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).flatten()
    return np.array([image_gray])

# Inference function
def classify_image(image_path):
    img = cv2.imread(image_path)
    img_preprocessed = preprocess_image(img)
    prediction = model.predict(img_preprocessed)
    return prediction[0]

# Test the inference
image_path = 'path_to_test_image.jpg'  # Change to your image path
print(f"Prediction: {classify_image(image_path)}")
