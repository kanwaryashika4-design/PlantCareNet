# 🌱 PlantCareNet: AI-Powered Smart Plant Doctor

An AI-powered web application for automated **tomato plant disease diagnosis**, **infection severity estimation**, and **soil nutrient deficiency prediction** using Deep Learning, Machine Learning, Computer Vision, and Explainable AI (XAI).

Developed during my Summer Research Internship at the **Department of Computer Science & Engineering, National Institute of Technology (NIT) Hamirpur**.

---

# 🚀 Features

## 👨‍🌾 Farmer Portal

- Tomato leaf disease detection using MobileNetV2
- Confidence score prediction
- HSV-based infection severity estimation
- Severity categorization (Mild, Moderate, Severe)
- Grad-CAM visualization for model explainability
- Disease information and treatment recommendations

---

## 👨‍🔬 Researcher Portal

- Soil nutrient deficiency prediction
- Random Forest-based classification
- SHAP global feature importance
- SHAP local prediction explanation
- Personalized nutrient recommendations

---

# 🧠 AI Models

### Disease Diagnosis Module

- Model: MobileNetV2 (Transfer Learning)
- Framework: TensorFlow/Keras
- Classes:
  - Healthy
  - Bacterial Spot
  - Early Blight
  - Late Blight

Accuracy: **94%**

---

### Nutrient Deficiency Module

- Model: Random Forest Classifier

Input Features:

- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- Soil pH
- Temperature
- Humidity

Accuracy: **96%**

---

# 💡 Explainable AI

### Grad-CAM

Used to highlight infected regions responsible for disease prediction.

### SHAP

Used for:

- Global Feature Importance
- Local Prediction Interpretation
- Feature Contribution Analysis

---

# 🖥️ Tech Stack

## Backend

- Python
- Flask
- TensorFlow
- Keras
- OpenCV
- Scikit-learn
- SHAP
- NumPy
- Pandas

## Frontend

- HTML5
- CSS3
- JavaScript

---

# 📂 Project Structure

```
PlantCareNet
│
├── backend
│   ├── models
│   │   ├── plant_doctor_high_accuracy.h5
│   │   ├── tomato_nutrient_stress_model.pkl
│   │   └── class_indices.json
│   │
│   ├── utils
│   │   ├── gradcam.py
│   │   ├── image_preprocessing.py
│   │   ├── nutrient_preprocessing.py
│   │   ├── recommendation_engine.py
│   │   ├── severity_scoring.py
│   │   └── shap_explainer.py
│   │
│   ├── app.py
│   ├── config.py
│   └── requirements.txt
│
├── frontend
│   ├── static
│   │   ├── css
│   │   ├── images
│   │   └── js
│   │
│   └── templates
│       ├── home.html
│       ├── farmer_portal.html
│       ├── researcher_portal.html
│       ├── disease_library.html
│       └── about.html
│
├── notebooks
│   ├── disease_model_training.ipynb
│   └── nutrient_model_training.ipynb
│
└── README.md
```

---

# 📊 Model Performance

| Module | Model | Accuracy |
|----------|----------|----------|
| Disease Classification | MobileNetV2 | **94%** |
| Nutrient Prediction | Random Forest | **96%** |

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/kanwaryashika4-design/PlantCareNet.git
```

Move into project directory

```bash
cd PlantCareNet
```

---

## Create Virtual Environment (Recommended)

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

# ▶️ Run the Project

Start the Flask server:

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

# 📸 Application Workflow

### Farmer Portal

1. Upload tomato leaf image.
2. AI detects disease.
3. Confidence score is generated.
4. Infection severity is estimated.
5. Grad-CAM highlights infected regions.
6. Treatment recommendation is displayed.

---

### Researcher Portal

1. Enter N, P, K, pH, Temperature and Humidity.
2. Random Forest predicts nutrient deficiency.
3. SHAP explains prediction.
4. Recommendation is generated.

---

# 🔮 Future Scope

- Support multiple crop species.
- Mobile application deployment.
- IoT sensor integration.
- Cloud-based disease monitoring.
- Real-time field surveillance.
- Multilingual support for farmers.

---

# 👩‍💻 Author

**Yashika Kanwar**

B.Tech Computer Science & Engineering (Artificial Intelligence & Machine Learning)

Research Intern

Department of Computer Science & Engineering

National Institute of Technology Hamirpur

---

# 📄 License

This project is developed for **academic and research purposes**.
