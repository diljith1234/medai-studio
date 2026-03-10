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

# --- IMPROVED PRE-PROCESSING ---
# This creates a list of the 131 unique symptoms the model actually knows.
def get_model_feature_names():
    # Get the 131 symptom names without the "Symptom_X_" prefix
    # We use a set to keep only unique names, then sort to maintain order
    unique_names = []
    for f in list(all_features):
        clean = "_".join(f.split("_")[2:]) if "Symptom_" in f else f
        clean = clean.strip()
        if clean not in unique_names:
            unique_names.append(clean)
    
    # Return exactly the number of features the model expects
    return unique_names[:model.n_features_in_]

# Pre-calculate the clean list once when the server starts
CLEAN_SYMPTOMS = get_model_feature_names()

@app.route("/api/main", methods=["GET", "POST"])
def handle_request():
    # --- 1. GET SYMPTOMS (For the Frontend Dropdown) ---
    if request.method == "GET":
        try:
            # We return the original 394-item list so your frontend logic stays the same
            return jsonify({"symptoms": list(all_features)})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # --- 2. PREDICT DISEASE (The Analyze Button) ---
    if request.method == "POST":
        try:
            data = request.get_json()
            selected_from_ui = data.get("symptoms", [])
            
            # Create a blank vector of 131 zeros
            input_vector = np.zeros(len(CLEAN_SYMPTOMS))
            
            for s in selected_from_ui:
                # Clean the incoming symptom (e.g., "Symptom_1_headache" -> "headache")
                clean_s = "_".join(s.split("_")[2:]) if "Symptom_" in s else s
                clean_s = clean_s.strip()

                # If that symptom exists in our model's vocabulary, flip the bit to 1
                if clean_s in CLEAN_SYMPTOMS:
                    idx = CLEAN_SYMPTOMS.index(clean_s)
                    input_vector[idx] = 1

            # Predict using the 131-length vector
            prediction_result = model.predict(input_vector.reshape(1, -1))[0]
            disease = str(prediction_result).strip()

            # Fetch Metadata (Description & Precautions)
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
            print(f"Prediction Error: {e}")
            return jsonify({"error": "Failed to process prediction"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)