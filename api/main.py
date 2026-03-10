from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

base_path = os.path.dirname(os.path.abspath(__file__))

# Load the NEW synced files
model = joblib.load(os.path.join(base_path, "model.pkl"))
all_features = joblib.load(os.path.join(base_path, "features.pkl"))
description_df = pd.read_csv(os.path.join(base_path, "symptom_Description.csv"))
precaution_df = pd.read_csv(os.path.join(base_path, "symptom_precaution.csv"))

@app.route("/api/main", methods=["GET", "POST"])
def handle_request():
    if request.method == "GET":
        # Returns clean names: ["itching", "skin_rash", "nodal_skin_eruptions", ...]
        return jsonify({"symptoms": all_features})

    if request.method == "POST":
        try:
            data = request.get_json()
            selected = data.get("symptoms", [])
            
            # Create vector based on the 131 symptoms
            input_vector = np.zeros(len(all_features))
            
            for s in selected:
                if s in all_features:
                    idx = all_features.index(s)
                    input_vector[idx] = 1

            prediction = model.predict(input_vector.reshape(1, -1))[0]
            disease = str(prediction).strip()

            desc = description_df[description_df['Disease'] == disease]['Description'].values
            description = desc[0] if len(desc) > 0 else "No description available."
            
            prec = precaution_df[precaution_df['Disease'] == disease].iloc[:, 1:].values
            precautions = [p for p in prec[0].tolist() if str(p) != 'nan' and p is not None] if len(prec) > 0 else []

            return jsonify({
                "prediction": disease,
                "description": description,
                "precautions": precautions
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)