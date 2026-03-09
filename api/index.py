from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

base_path = os.path.dirname(os.path.abspath(__file__))

# Load AI Model
model = joblib.load(os.path.join(base_path, "model.pkl"))
all_features = joblib.load(os.path.join(base_path, "features.pkl"))

# Load Knowledge Base (Kaggle CSVs)
description_df = pd.read_csv(os.path.join(base_path, "symptom_Description.csv"))
precaution_df = pd.read_csv(os.path.join(base_path, "symptom_precaution.csv"))

@app.route("/symptoms", methods=["GET"])
def get_symptoms():
    return jsonify({"symptoms": all_features})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        selected_symptoms = data.get("symptoms", [])
        input_vector = np.zeros(len(all_features))
        
        for s in selected_symptoms:
            if s in all_features:
                idx = list(all_features).index(s)
                input_vector[idx] = 1

        # 1. Get Prediction
        disease = model.predict(input_vector.reshape(1, -1))[0].strip()

        # 2. Get Description
        desc = description_df[description_df['Disease'] == disease]['Description'].values
        description = desc[0] if len(desc) > 0 else "No description available."

        # 3. Get Precautions
        prec = precaution_df[precaution_df['Disease'] == disease].iloc[:, 1:].values
        precautions = prec[0].tolist() if len(prec) > 0 else []
        precautions = [p for p in precautions if str(p) != 'nan']

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