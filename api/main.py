from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Dynamically find the path so Vercel can find your files
base_path = os.path.dirname(os.path.abspath(__file__))

# Load AI Model
model = joblib.load(os.path.join(base_path, "model.pkl"))
all_features = joblib.load(os.path.join(base_path, "features.pkl"))

# Load Knowledge Base (Kaggle CSVs)
description_df = pd.read_csv(os.path.join(base_path, "symptom_Description.csv"))
precaution_df = pd.read_csv(os.path.join(base_path, "symptom_precaution.csv"))

# --- PRE-PROCESSING THE FEATURES ---
# Your model expects 131 features. We need to extract the "unique" 131 symptom names
# from the 394 list (removing 'Symptom_1_', etc.)
def get_clean_feature_list():
    raw_names = []
    for f in list(all_features):
        # Cleans 'Symptom_1_itching' -> 'itching'
        clean_name = "_".join(f.split("_")[2:]) if "Symptom_" in f else f
        raw_names.append(clean_name.strip())
    
    # We take only the first 131 to match the model's training
    return raw_names[:model.n_features_in_]

CLEAN_FEATURES = get_clean_feature_list()

@app.route("/api/main", methods=["GET", "POST"])
def handle_request():
    # --- 1. HANDLE SYMPTOM LIST REQUEST (GET) ---
    if request.method == "GET":
        try:
            # We send the original 394 list so the Frontend matches what you see in the pickle
            return jsonify({"symptoms": list(all_features)})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # --- 2. HANDLE PREDICTION REQUEST (POST) ---
    if request.method == "POST":
        try:
            data = request.get_json()
            selected_symptoms = data.get("symptoms", [])
            
            # Initialize input vector with exactly 131 zeros (matching the model)
            input_vector = np.zeros(len(CLEAN_FEATURES))
            
            # Map selected symptoms to the input vector
            for s in selected_symptoms:
                # Clean the incoming symptom name to match our feature list
                clean_s = "_".join(s.split("_")[2:]) if "Symptom_" in s else s
                clean_s = clean_s.strip()

                if clean_s in CLEAN_FEATURES:
                    idx = CLEAN_FEATURES.index(clean_s)
                    input_vector[idx] = 1

            # Get Prediction from Random Forest Model
            # Reshape to (1, 131)
            prediction_result = model.predict(input_vector.reshape(1, -1))[0]
            disease = str(prediction_result).strip()

            # Get Description from CSV
            desc = description_df[description_df['Disease'] == disease]['Description'].values
            description = desc[0] if len(desc) > 0 else "No description available."

            # Get Precautions from CSV
            prec = precaution_df[precaution_df['Disease'] == disease].iloc[:, 1:].values
            precautions = [p for p in prec[0].tolist() if str(p) != 'nan' and p is not None] if len(prec) > 0 else []

            return jsonify({
                "prediction": disease,
                "description": description,
                "precautions": precautions,
                "status": "success"
            })
        except Exception as e:
            # Printing error to Vercel logs for easier debugging
            print(f"Prediction Error: {e}")
            return jsonify({"error": str(e)}), 500

# Required for Vercel
if __name__ == "__main__":
    app.run(port=5000, debug=True)