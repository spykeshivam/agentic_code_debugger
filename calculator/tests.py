# tests.py

import unittest
from pkg.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_addition(self):
        result = self.calculator.evaluated("3 + 5")
        self.assertEqual(result, 8)

    def test_subtraction(self):
        result = self.calculator.evaluated("10 - 4")
        self.assertEqual(result, 6)

    def test_multiplication(self):
        result = self.calculator.evaluated("3 * 4")
        self.assertEqual(result, 12)

    def test_division(self):
        result = self.calculator.evaluated("10 / 2")
        self.assertEqual(result, 5)

    def test_nested_expression(self):
        result = self.calculator.evaluated("3 * 4 + 5")
        self.assertEqual(result, 17)

    def test_complex_expression(self):
        result = self.calculator.evaluated("2 * 3 - 8 / 2 + 5")
        self.assertEqual(result, 7)

    def test_empty_expression(self):
        result = self.calculator.evaluated("")
        self.assertIsNone(result)

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluated("$ 3 5")

    def test_not_enough_operands(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluated("+ 3")


if __name__ == "__main__":
    unittest.main()
