import unittest
from health_utils import calculate_bmi, calculate_bmr

class TestHealthCalculations(unittest.TestCase):
    def test_calculate_bmi(self):
        # Test BMI calculation: weight 70kg and height 1.75m should be ~22.86
        height = 1.75
        weight = 70
        calculated_bmi = calculate_bmi(height, weight)
        print(f"\nBMI Test:  Height={height:<4}m, Weight={weight:<3}kg -> Calculated BMI: {calculated_bmi:.2f}")
        self.assertAlmostEqual(calculated_bmi, 22.86, places=2)

    def test_calculate_bmr_male(self):
        # Test BMR calculation for a male
        height = 175
        weight = 70
        age = 25
        gender = 'male'
        calculated_bmr = calculate_bmr(height, weight, age, gender)
        expected_bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        print(f"BMR Test ({gender.capitalize():<6}): Height={height:<3}cm, Weight={weight:<3}kg, Age={age:<3} -> Calculated BMR: {calculated_bmr:.2f}")
        self.assertAlmostEqual(calculated_bmr, expected_bmr, places=2)

    def test_calculate_bmr_female(self):
        # Test BMR calculation for a female
        height = 165
        weight = 60
        age = 30
        gender = 'female'
        calculated_bmr = calculate_bmr(height, weight, age, gender)
        expected_bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        print(f"BMR Test ({gender.capitalize():<6}): Height={height:<3}cm, Weight={weight:<3}kg, Age={age:<3} -> Calculated BMR: {calculated_bmr:.2f}")
        self.assertAlmostEqual(calculated_bmr, expected_bmr, places=2)

if __name__ == '__main__':
    unittest.main()