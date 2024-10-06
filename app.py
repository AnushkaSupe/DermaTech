from flask import Flask, request, jsonify, render_template
from keras.models import load_model
from PIL import Image
import numpy as np
import os

app = Flask(__name__)

# Load your trained model
model = load_model('skin_issue_model.keras')

# Define input shape for the model
input_width, input_height, num_channels = 224, 224, 3  # Adjust these according to your model

def preprocess_image(image_path):
    # Load image
    img = Image.open(image_path)

    # Resize the image to the expected input shape of the model
    img = img.resize((input_width, input_height), Image.LANCZOS)  # Match the input shape

    # Convert image to array and normalize
    img_array = np.array(img) / 255.0  # Normalize pixel values to [0, 1]
    
    # Ensure the array has 3 channels (RGB)
    if img_array.shape[-1] != 3:
        img_array = np.stack((img_array,) * 3, axis=-1)  # Convert grayscale to RGB if needed

    img_array = img_array.reshape((1, input_width, input_height, num_channels))  # Reshape for the model

    return img_array

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Check if an image file was uploaded
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        # Save the uploaded image
        file = request.files['image']
        file_path = 'temp_image.jpg'  # Temporary path for processing
        file.save(file_path)

        # Preprocess the image
        processed_image = preprocess_image(file_path)

        # Make prediction
        prediction = model.predict(processed_image)

        # Process the prediction output (adjust this according to your model's output)
        skin_issue = np.argmax(prediction)  # Assuming a classification model

        # Clean up the temporary image
        os.remove(file_path)

        return jsonify({'skin_issue': skin_issue})

    except Exception as e:
        app.logger.error(f'Error in predicting: {e}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
