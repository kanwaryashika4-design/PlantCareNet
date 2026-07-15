import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

DISEASE_MODEL_PATH = os.path.join(MODELS_DIR, 'plant_doctor_high_accuracy.h5')
NUTRIENT_MODEL_PATH = os.path.join(MODELS_DIR, 'tomato_nutrient_stress_model.pkl')
CLASS_INDICES_PATH = os.path.join(MODELS_DIR, 'class_indices.json')

IMG_SIZE = (224, 224)
MAX_UPLOAD_SIZE_MB = 10
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

N_TARGET = 80
P_TARGET = 50
K_TARGET = 50