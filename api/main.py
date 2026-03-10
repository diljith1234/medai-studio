from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

base_path = os.path.dirname(os.path.abspath(__file__))

# Load AI Model and the original feature list
model = joblib.load(os.path.join(base_path, "model.pkl"))
all_features = joblib.load(os.path.join(base_path, "features.pkl"))

# Load Knowledge Base
description_df = pd.read_csv(os.path.join(base_path, "symptom_Description.csv"))
precaution_df = pd.read_csv(os.path.join(base_path, "symptom_precaution.csv"))

# --- THE FIX: MANUAL FEATURE RE-ORDERING ---
def get_clean_vocab():
    # We need to extract the unique 131 symptom names in the order they appear
    # in the dataset. Since the dataset was likely 'flat', we take the unique 
    # names while preserving the order of their first appearance.
    seen = set()
    ordered_unique = []
    for f in all_features:
        # Strip 'Symptom_1_', 'Symptom_2_', etc.
        clean = "_".join(f.split("_")[2:]) if "Symptom_" in f else f
        clean = clean.strip().lower()
        if clean not in seen:
            ordered_unique.append(clean)
            seen.add(clean)
    
    # Return exactly the 131 symptoms the model was built for
    return ordered_unique[:131]

VOCAB = get_clean_vocab()

@app.route("/api/main", methods=["GET", "POST"])
def handle_request():
    if request.method == "GET":
        return jsonify({"symptoms": list(all_features)})

    if request.method == "POST":
        try:
            data = request.get_json()
            user_selections = data.get("symptoms", [])
            
            # Create a vector of exactly 131 zeros
            # If your model specifically requires 131, this MUST be 131.
            input_vector = np.zeros(131)
            
            for s in user_selections:
                # Clean the symptom from the UI
                clean_s = "_".join(s.split("_")[2:]) if "Symptom_" in s else s
                clean_s = clean_s.strip().lower()

                # Check against our VOCAB
                if clean_s in VOCAB:
                    idx = VOCAB.index(clean_s)
                    input_vector[idx] = 1

            # --- DEBUGGING LOG (See this in Vercel Runtime Logs) ---
            print(f"Selected: {user_selections} -> Vector Indices: {np.where(input_vector == 1)}")

            prediction = model.predict(input_vector.reshape(1, -1))[0]
            disease = str(prediction).strip()

            # Metadata Lookup
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
            print(f"ERROR: {str(e)}")
            return jsonify({"error": "Prediction failed"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)