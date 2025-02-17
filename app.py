# app.py
from flask import Flask, request, jsonify, render_template
from utilities import update_xgboost_model, validate_new_data
import pandas as pd
import joblib
import os

app = Flask(__name__)
model = None
model_path = os.path.join(os.getcwd(), "models", "updated_pipeline.pkl")
# Load the model at startup
try:
    model = joblib.load(model_path)
except Exception as e:
    print(f"Error loading model: {str(e)}")
    model = None

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/predict', methods=['POST'])
def predict():
    try:
        if request.is_json:
            # Case 1: JSON data received
            data = request.get_json()
        else:
            # Case 2: Form data received
            data = {
                "Cement": float(request.form["Cement"]),
                "Slag": float(request.form["Slag"]),
                "Ash": float(request.form["Ash"]),
                "Water": float(request.form["Water"]),
                "Plast": float(request.form["Plast"]),
                "Coarse": float(request.form["Coarse"]),
                "Fine": float(request.form["Fine"]),
                "Days": float(request.form["Days"]),
                "WC": float(request.form["WC"])
            }
# Convert to DataFrame
        input_data = pd.DataFrame([data])

        # Check if model is loaded
        if model is None:
            return jsonify({"status": "error", "message": "Model not loaded"}), 500

        # Make prediction
        prediction = model.predict(input_data)[0]

        if request.is_json:
            # Return JSON response if the request was JSON
            return jsonify({"status": "success", "prediction": round(float(prediction), 2)})
        else:
            # Return HTML page with prediction
            return render_template('index.html', prediction=round(float(prediction), 2))
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400   

if __name__ == '__main__':
    app.run(debug=True, port=8000)
app = Flask(__name__, template_folder="templates")

