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

# Load AI Model - Using absolute paths for Vercel stability
model = joblib.load(os.path.join(base_path, "model.pkl"))
all_features = joblib.load(os.path.join(base_path, "features.pkl"))

# Load Knowledge Base (Kaggle CSVs)
description_df = pd.read_csv(os.path.join(base_path, "symptom_Description.csv"))
precaution_df = pd.read_csv(os.path.join(base_path, "symptom_precaution.csv"))

@app.route("/api/main", methods=["GET", "POST"])
def handle_request():
    # --- 1. HANDLE SYMPTOM LIST REQUEST (GET) ---
    if request.method == "GET":
        try:
            symptoms_list = list(all_features)
            return jsonify({"symptoms": symptoms_list})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # --- 2. HANDLE PREDICTION REQUEST (POST) ---
    if request.method == "POST":
        try:
            data = request.get_json()
            selected_symptoms = data.get("symptoms", [])
            
            # Initialize input vector with zeros
            input_vector = np.zeros(len(all_features))
            
            # Map selected symptoms to the input vector
            for s in selected_symptoms:
                if s in all_features:
                    idx = list(all_features).index(s)
                    input_vector[idx] = 1

            # Get Prediction from Random Forest Model
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
            return jsonify({"error": str(e)}), 500

# Required for Vercel
if __name__ == "__main__":
    app.run(port=5000, debug=True)