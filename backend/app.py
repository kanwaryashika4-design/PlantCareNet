import os
import sys
import json
import numpy as np
import joblib
import tensorflow as tf
from flask import Flask, render_template, request, jsonify

from PIL import Image
import io

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (DISEASE_MODEL_PATH, NUTRIENT_MODEL_PATH,
                    CLASS_INDICES_PATH, ALLOWED_EXTENSIONS)
from utils.image_preprocessing import preprocess_image, validate_is_tomato_leaf
from utils.severity_scoring import calculate_severity
from utils.nutrient_preprocessing import engineer_nutrient_features
from utils.recommendation_engine import (get_disease_recommendation,
                                         get_nutrient_recommendation)
from utils.gradcam import generate_gradcam, get_all_class_probabilities
from utils.shap_explainer import generate_shap_chart

app = Flask(
    __name__,
    template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'templates')),
    static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static'))
)

# Load models once at startup
print("Loading models...")
disease_model = tf.keras.models.load_model(DISEASE_MODEL_PATH)
nutrient_model = joblib.load(NUTRIENT_MODEL_PATH)

with open(CLASS_INDICES_PATH) as f:
    raw_indices = json.load(f)
    class_indices = {int(k): v for k, v in raw_indices.items()}

print("Models loaded:", class_indices)


def allowed_file(filename):
    return ('.' in filename and
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/farmer')
def farmer_portal():
    return render_template('farmer_portal.html')


@app.route('/researcher')
def researcher_portal():
    return render_template('researcher_portal.html')


@app.route('/disease-library')
def disease_library():
    return render_template('disease_library.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/predict/disease', methods=['POST'])
def predict_disease():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({
            'error': 'Invalid file type. Please upload JPG, PNG, or WEBP'
        }), 400

    try:
        file_bytes = file.read()
        file_stream = io.BytesIO(file_bytes)

        img_array, pil_img = preprocess_image(file_stream)

        predictions = disease_model.predict(img_array, verbose=0)
        predicted_index = int(np.argmax(predictions[0]))
        confidence = round(float(np.max(predictions[0])) * 100, 2)
        disease_label = class_indices[predicted_index]

        # Validate it is a tomato leaf
        is_valid, reasons = validate_is_tomato_leaf(pil_img, confidence)

        if not is_valid:
            return jsonify({
                'success': False,
                'invalid_image': True,
                'reasons': reasons,
                'message': 'Invalid image. Please upload a clear tomato leaf photo.',
                'tips': [
                    'Use a clear, well-lit photo of a tomato leaf',
                    'Ensure the leaf fills most of the frame',
                    'Avoid photos of other plants, objects, or documents',
                    'Plant Care Net is trained for tomato leaves only'
                ]
            }), 200

        is_healthy = disease_label.lower() == 'healthy'
        display_name = disease_label.replace('_', ' ').title()

        # Severity scoring — only for diseased leaves
        severity_pct, severity_bucket = calculate_severity(
            pil_img, disease_label)

        # Treatment recommendation
        recommendation = get_disease_recommendation(disease_label)

        # Grad-CAM heatmap
        gradcam_image = generate_gradcam(
            disease_model, img_array, predicted_index, pil_img)

        # All class probabilities
        all_probs = get_all_class_probabilities(predictions, class_indices)

        return jsonify({
            'success': True,
            'disease': display_name,
            'disease_raw': disease_label,
            'confidence': confidence,
            'severity_percentage': severity_pct,
            'severity_level': severity_bucket,
            'treatment': recommendation['treatment'],
            'priority': recommendation['priority'],
            'timeframe': recommendation['timeframe'],
            'severity_color': recommendation['severity_color'],
            'is_healthy': is_healthy,
            'gradcam_image': gradcam_image,
            'all_probabilities': all_probs
        })

    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500


@app.route('/predict/nutrient', methods=['POST'])
def predict_nutrient():
    try:
        data = request.get_json()

        required_fields = ['N', 'P', 'K', 'temperature', 'humidity', 'ph']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400

        n = float(data['N'])
        p = float(data['P'])
        k = float(data['K'])
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        ph = float(data['ph'])

        if not (0 <= n <= 140):
            return jsonify(
                {'error': 'Nitrogen (N) must be between 0 and 140'}), 400
        if not (0 <= p <= 145):
            return jsonify(
                {'error': 'Phosphorus (P) must be between 0 and 145'}), 400
        if not (0 <= k <= 205):
            return jsonify(
                {'error': 'Potassium (K) must be between 0 and 205'}), 400
        if not (0 <= temperature <= 50):
            return jsonify(
                {'error': 'Temperature must be between 0 and 50°C'}), 400
        if not (0 <= humidity <= 100):
            return jsonify(
                {'error': 'Humidity must be between 0 and 100%'}), 400
        if not (0 <= ph <= 14):
            return jsonify({'error': 'pH must be between 0 and 14'}), 400

        features = engineer_nutrient_features(
            n, p, k, temperature, humidity, ph)
        features_array = np.array([features])

        prediction = nutrient_model.predict(features_array)[0]
        probabilities = nutrient_model.predict_proba(features_array)[0]
        confidence = round(float(np.max(probabilities)) * 100, 2)

        # All class probabilities for nutrient
        all_nutrient_probs = []
        for cls, prob in zip(nutrient_model.classes_, probabilities):
            all_nutrient_probs.append({
                'label': cls.replace('_', ' '),
                'probability': round(float(prob) * 100, 2)
            })
        all_nutrient_probs.sort(
            key=lambda x: x['probability'], reverse=True)

        # SHAP explanation chart
        shap_chart = generate_shap_chart(
            nutrient_model, features_array, prediction)

        recommendation = get_nutrient_recommendation(prediction)

        return jsonify({
            'success': True,
            'nutrient_status': prediction.replace('_', ' '),
            'nutrient_raw': prediction,
            'confidence': confidence,
            'treatment': recommendation['treatment'],
            'priority': recommendation['priority'],
            'timeframe': recommendation['timeframe'],
            'severity_color': recommendation['severity_color'],
            'shap_chart': shap_chart,
            'all_probabilities': all_nutrient_probs
        })

    except ValueError as e:
        return jsonify({'error': f'Invalid input values: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)