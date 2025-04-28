# Add render_template to the imports
from flask import Flask, request, jsonify, render_template
from models import BMIInput, BMRInput
from health_utils import calculate_bmi, calculate_bmr

app = Flask(__name__)

@app.route('/')
def index():
    """Serve the HTML testing page from the templates folder."""
    # Use render_template to find and return index.html
    return render_template('index.html')

@app.route('/bmi', methods=['POST'])
def bmi():
    """
    Calculate Body Mass Index (BMI) using height (meters) and weight (kg).
    """
    try:
        data = request.get_json()
        # Input validation using Pydantic model
        bmi_input = BMIInput(**data)
        bmi_value = calculate_bmi(bmi_input.height, bmi_input.weight)
        return jsonify({'bmi': round(bmi_value, 2)}), 200
    # Catch Pydantic's validation errors specifically if desired,
    # or keep general Exception for broader coverage.
    # from pydantic import ValidationError
    # except ValidationError as e:
    #    return jsonify({'error': e.errors()}), 400
    except Exception as e:
        # Return a meaningful error message
        return jsonify({'error': f"Invalid input: {e}"}), 400

@app.route('/bmr', methods=['POST'])
def bmr():
    """
    Calculate Basal Metabolic Rate (BMR) using height (cm), weight (kg), age, and gender.
    """
    try:
        data = request.get_json()
        # Input validation using Pydantic model
        bmr_input = BMRInput(**data)
        bmr_value = calculate_bmr(bmr_input.height, bmr_input.weight, bmr_input.age, bmr_input.gender)
        return jsonify({'bmr': round(bmr_value, 2)}), 200
    # Catch Pydantic's validation errors specifically if desired
    # from pydantic import ValidationError
    # except ValidationError as e:
    #    return jsonify({'error': e.errors()}), 400
    except Exception as e:
         # Return a meaningful error message
        return jsonify({'error': f"Invalid input: {e}"}), 400

if __name__ == '__main__':
    # Host 0.0.0.0 makes it accessible externally (within Docker network)
    # Port 5001 matches Dockerfile EXPOSE and docker-compose ports
    app.run(host='0.0.0.0', port=5001)