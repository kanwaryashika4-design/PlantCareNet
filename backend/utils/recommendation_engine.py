DISEASE_TREATMENTS = {
    "Bacterial_spot": {
        "treatment": "Apply copper-based bactericide (Copper Oxychloride 50% WP). Remove and destroy infected leaves. Avoid overhead irrigation to reduce leaf wetness.",
        "priority": "High Priority",
        "timeframe": "Treat within 24 hours",
        "severity_color": "red"
    },
    "Early_blight": {
        "treatment": "Apply chlorothalonil or mancozeb-based fungicide. Ensure adequate plant spacing for air circulation. Remove lower infected leaves.",
        "priority": "Moderate Priority",
        "timeframe": "Treat within 48 hours",
        "severity_color": "orange"
    },
    "Late_blight": {
        "treatment": "Apply copper fungicide immediately. Remove and destroy all infected plant material. Avoid working in wet fields to prevent spread.",
        "priority": "High Priority",
        "timeframe": "Treat within 24 hours",
        "severity_color": "red"
    },
    "healthy": {
        "treatment": "No disease detected. Your tomato plant appears healthy. Maintain current care routine with regular watering and balanced fertilization.",
        "priority": "No Action Required",
        "timeframe": "Continue routine monitoring",
        "severity_color": "green"
    }
}

NUTRIENT_TREATMENTS = {
    "Nitrogen_Deficiency": {
        "treatment": "Apply nitrogen-rich fertilizer such as Urea (46-0-0) or Ammonium Sulfate. Recommended dosage: 20-25 kg/acre. Apply in split doses for best absorption.",
        "priority": "High Priority",
        "timeframe": "Apply within 3-5 days",
        "severity_color": "red"
    },
    "Phosphorus_Deficiency": {
        "treatment": "Apply Single Super Phosphate (SSP) or Di-Ammonium Phosphate (DAP). Recommended dosage: 15-20 kg/acre. Best applied near root zone.",
        "priority": "Moderate Priority",
        "timeframe": "Apply within 7 days",
        "severity_color": "orange"
    },
    "Potassium_Deficiency": {
        "treatment": "Apply Potassium Sulfate (SOP) or Muriate of Potash (MOP). Recommended dosage: 15-20 kg/acre. Avoid over-application which can lock out other nutrients.",
        "priority": "Moderate Priority",
        "timeframe": "Apply within 7 days",
        "severity_color": "orange"
    },
    "Healthy_Nutrients": {
        "treatment": "No deficiency detected. All nutrient levels are within optimal range. Maintain current fertilization schedule and continue regular soil pH monitoring.",
        "priority": "No Action Required",
        "timeframe": "Continue routine monitoring",
        "severity_color": "green"
    }
}

def get_disease_recommendation(disease_label):
    return DISEASE_TREATMENTS.get(disease_label, {
        "treatment": "Consult a local agronomist for manual diagnosis.",
        "priority": "Manual Review Required",
        "timeframe": "As soon as possible",
        "severity_color": "gray"
    })

def get_nutrient_recommendation(nutrient_label):
    return NUTRIENT_TREATMENTS.get(nutrient_label, {
        "treatment": "Consult a local agronomist for soil testing.",
        "priority": "Manual Review Required",
        "timeframe": "As soon as possible",
        "severity_color": "gray"
    })