import unittest
from health_utils import calculate_bmi, calculate_bmr

class TestHealthCalculations(unittest.TestCase):
    def test_calculate_bmi(self):
        # Test BMI calculation: weight 70kg and height 1.75m should be ~22.86
        self.assertAlmostEqual(calculate_bmi(1.75, 70), 22.86, places=2)

    def test_calculate_bmr_male(self):
        # Test BMR calculation for a male
        expected_bmr = 88.362 + (13.397 * 70) + (4.799 * 175) - (5.677 * 25)
        self.assertAlmostEqual(calculate_bmr(175, 70, 25, 'male'), expected_bmr, places=2)

    def test_calculate_bmr_female(self):
        # Test BMR calculation for a female
        expected_bmr = 447.593 + (9.247 * 60) + (3.098 * 165) - (4.330 * 30)
        self.assertAlmostEqual(calculate_bmr(165, 60, 30, 'female'), expected_bmr, places=2)

if __name__ == '__main__':
    unittest.main()
