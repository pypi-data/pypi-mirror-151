# test_arithmetic.py
import myarithmetic80589
import unittest
class TestArithmetic(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(myarithmetic80589.add(1, 2), 3)
    def test_subtraction(self):
        self.assertEqual(myarithmetic80589.subtract(2, 1), 1)
    def test_multiplication(self):
        self.assertEqual(myarithmetic80589.multiply(5, 5), 25)
    def test_division(self):
        self.assertEqual(myarithmetic80589.divide(8, 2), 4)
if __name__ == '__main__':
    unittest.main()