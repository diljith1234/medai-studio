from flask import Flask, request, jsonify, render_template
import pickle
import os

app = Flask(__name__)

# Load model
model = pickle.load(open("model.pkl", "rb"))
feature_names = pickle.load(open("features.pkl", "rb"))

# Extract clean symptom names
symptoms_list = []

for feature in feature_names:
    parts = feature.split("_")
    symptom = "_".join(parts[2:])
    symptoms_list.append(symptom.strip())

symptoms_list = sorted(list(set(symptoms_list)))

@app.route("/")
def home():
    return render_template("index.html", symptoms=symptoms_list)

@app.route("/predict", methods=["POST"])
def predict():

    selected_symptoms = request.form.getlist("symptoms")

    input_vector = [0] * len(feature_names)

    for symptom in selected_symptoms:
        for i, feature in enumerate(feature_names):
            if symptom in feature:
                input_vector[i] = 1

    prediction = model.predict([input_vector])[0]

    return render_template("index.html",
                           prediction=prediction,
                           symptoms=symptoms_list)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
