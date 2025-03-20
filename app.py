from flask import Flask, request, jsonify
from models import BMIInput, BMRInput
from health_utils import calculate_bmi, calculate_bmr

app = Flask(__name__)

@app.route('/bmi', methods=['POST'])
def bmi():
    """
    Calculate Body Mass Index (BMI) using height (meters) and weight (kg).
    Expects JSON payload:
    {
        "height": <float>,  // in meters
        "weight": <float>   // in kilograms
    }
    """
    try:
        data = request.get_json()
        bmi_input = BMIInput(**data)
        bmi_value = calculate_bmi(bmi_input.height, bmi_input.weight)
        return jsonify({'bmi': round(bmi_value, 2)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/bmr', methods=['POST'])
def bmr():
    """
    Calculate Basal Metabolic Rate (BMR) using height (cm), weight (kg), age, and gender.
    Expects JSON payload:
    {
        "height": <float>,  // in centimeters
        "weight": <float>,  // in kilograms
        "age": <int>,       // in years
        "gender": <str>     // "male" or "female"
    }
    """
    try:
        data = request.get_json()
        bmr_input = BMRInput(**data)
        bmr_value = calculate_bmr(bmr_input.height, bmr_input.weight, bmr_input.age, bmr_input.gender)
        return jsonify({'bmr': round(bmr_value, 2)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
