from flask import Flask, jsonify, request, render_template
import numpy as np
import pickle
import os

app = Flask(__name__)

# -----------------------------
# Load ML Model
# -----------------------------
MODEL_PATH = "random_forest_model.pkl"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("Model file not found: random_forest_model.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

print("✅ Model loaded successfully")

# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Health Check
# -----------------------------
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify(status="ok"), 200


# -----------------------------
# Prediction Endpoint
# -----------------------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        feature_names = [
            'FA (kg/m3)', 'GGBFS (kg/m3)', 'Coarse aggregate (kg/m3)',
            'Fine aggregate (kg/m3)', 'Na2SiO3', 'NaOH', 'Na2O (Dry)',
            'Sio2 (Dry)', 'Water (1)', 'Concentration (M) NaOH',
            'Water (2)', 'NaOH (Dry)', 'Additional water',
            'Superplasticizer', 'Total water',
            'Initial curing time (day)', 'Initial curing temp (C)',
            'Initial curing rest time (day)', 'Final curing temp (C)'
        ]

        # Accept JSON only
        if not request.is_json:
            return jsonify(error="Content-Type must be application/json"), 415

        data = request.get_json()

        features = []
        for feature in feature_names:
            if feature not in data:
                return jsonify(error=f"Missing feature: {feature}"), 400
            try:
                features.append(float(data[feature]))
            except ValueError:
                return jsonify(error=f"Invalid value for {feature}"), 400

        prediction = model.predict(np.array([features]))
        return jsonify(prediction=round(float(prediction[0]), 2))

    except Exception as e:
        return jsonify(error=str(e)), 500


# -----------------------------
# Run Flask App
# -----------------------------
if __name__ == "__main__":
    print("🚀 Starting Flask server...")
    app.run(debug=True)
