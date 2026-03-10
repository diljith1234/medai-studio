from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

base_path = os.path.dirname(os.path.abspath(__file__))

# Load AI Model and Features
model = joblib.load(os.path.join(base_path, "model.pkl"))
all_features = joblib.load(os.path.join(base_path, "features.pkl"))

# Load Knowledge Base
description_df = pd.read_csv(os.path.join(base_path, "symptom_Description.csv"))
precaution_df = pd.read_csv(os.path.join(base_path, "symptom_precaution.csv"))

# --- CRITICAL FIX: EXACT FEATURE MAPPING ---
def get_model_features():
    # We need the 131 unique symptoms in the EXACT order the model was trained on.
    # We strip the 'Symptom_X_' prefix and keep unique values.
    unique_list = []
    for f in list(all_features):
        clean = "_".join(f.split("_")[2:]) if "Symptom_" in f else f
        clean = clean.strip().lower()
        if clean not in unique_list:
            unique_list.append(clean)
    
    # Return exactly the 131 symptoms the model expects
    return unique_list[:131]

# Save this list so we use it for every prediction
MODEL_VOCABULARY = get_model_features()

@app.route("/api/main", methods=["GET", "POST"])
def handle_request():
    if request.method == "GET":
        return jsonify({"symptoms": list(all_features)})

    if request.method == "POST":
        try:
            data = request.get_json()
            selected_ui_symptoms = data.get("symptoms", [])
            
            # Create a vector of 131 zeros
            input_vector = np.zeros(131)
            
            for s in selected_ui_symptoms:
                # Clean the symptom from the UI (e.g., "Symptom_1_headache" -> "headache")
                clean_s = "_".join(s.split("_")[2:]) if "Symptom_" in s else s
                clean_s = clean_s.strip().lower()

                # Find its correct position in the 131-item list
                if clean_s in MODEL_VOCABULARY:
                    idx = MODEL_VOCABULARY.index(clean_s)
                    input_vector[idx] = 1

            # Predict
            prediction_result = model.predict(input_vector.reshape(1, -1))[0]
            disease = str(prediction_result).strip()

            # Get Description and Precautions
            desc = description_df[description_df['Disease'] == disease]['Description'].values
            description = desc[0] if len(desc) > 0 else "No description available."

            prec = precaution_df[precaution_df['Disease'] == disease].iloc[:, 1:].values
            precautions = [p for p in prec[0].tolist() if str(p) != 'nan' and p is not None] if len(prec) > 0 else []

            return jsonify({
                "prediction": disease,
                "description": description,
                "precautions": precautions,
                "status": "success"
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)