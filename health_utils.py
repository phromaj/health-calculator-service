def calculate_bmi(height: float, weight: float) -> float:
    """
    Calculate Body Mass Index (BMI).
    BMI = weight (kg) / (height (m))^2 [cite: 23]
    """
    if height <= 0:
        raise ValueError("Height must be greater than zero.")
    return weight / (height ** 2)

def calculate_bmr(height: float, weight: float, age: int, gender: str) -> float:
    """
    Calculate Basal Metabolic Rate (BMR) using the Harris-Benedict equation. [cite: 24]
    For males:
      BMR = 88.362 + (13.397 * weight in kg) + (4.799 * height in cm) - (5.677 * age in years) [cite: 24]

    For females:
      BMR = 447.593 + (9.247 * weight in kg) + (3.098 * height in cm) - (4.330 * age in years) [cite: 24]
    """
    if gender == 'male':
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender == 'female':
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age) # [cite: 25]
    else:
        raise ValueError("Gender must be 'male' or 'female'.")