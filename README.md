# 🌿 AI Tomato Plant Doctor

Smart AI-powered plant health assessment system for tomato crops.

## Features
- **Farmer Portal**: Upload leaf image → disease classification + severity scoring + treatment
- **Researcher Portal**: Enter N, P, K, pH, temperature, humidity → nutrient deficiency prediction + fertilizer recommendation

## Models
- Disease: MobileNetV2 (93.88% accuracy, 4 classes)
- Nutrient: Random Forest Classifier (96.36% accuracy, 4 classes)

## Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Then open http://localhost:5000

## Project Structure
```
smart-agriculture/
├── backend/          # Flask app + ML models + utilities
├── frontend/         # HTML templates + CSS + JS
└── notebooks/        # Training notebooks reference
```