"""
test_unittest.py - Unittest tests for calculator.py
"""

import unittest
import sys
import os

# Add the parent directory to path so we can import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.calculator import fun1, fun2, fun3, fun4, fun5, fun6, fun7


class TestCalculator(unittest.TestCase):

    def test_fun1(self):
        """Test addition function"""
        self.assertEqual(fun1(2, 3), 5)
        self.assertEqual(fun1(-1, 1), 0)
        self.assertEqual(fun1(0, 0), 0)

    def test_fun2(self):
        """Test subtraction function"""
        self.assertEqual(fun2(5, 3), 2)
        self.assertEqual(fun2(0, 5), -5)
        self.assertEqual(fun2(10, 10), 0)

    def test_fun3(self):
        """Test multiplication function"""
        self.assertEqual(fun3(3, 4), 12)
        self.assertEqual(fun3(-2, 3), -6)
        self.assertEqual(fun3(0, 100), 0)

    def test_fun4(self):
        """Test combined function"""
        self.assertEqual(fun4(2, 3), 10)
        self.assertEqual(fun4(0, 0), 0)

    def test_fun5(self):
        """Test division function"""
        self.assertEqual(fun5(10, 2), 5.0)
        self.assertEqual(fun5(-9, 3), -3.0)
        self.assertEqual(fun5(7, 2), 3.5)

    def test_fun5_divide_by_zero(self):
        """Test division raises ValueError on divide by zero"""
        with self.assertRaises(ValueError):
            fun5(10, 0)

    def test_fun6(self):
        """Test power function"""
        self.assertEqual(fun6(2, 3), 8)
        self.assertEqual(fun6(5, 0), 1)
        self.assertEqual(fun6(3, 2), 9)
        self.assertEqual(fun6(2, -1), 0.5)

    def test_fun7(self):
        """Test modulo function"""
        self.assertEqual(fun7(10, 3), 1)
        self.assertEqual(fun7(20, 5), 0)
        self.assertEqual(fun7(7, 4), 3)

    def test_fun7_mod_by_zero(self):
        """Test modulo raises ValueError on mod by zero"""
        with self.assertRaises(ValueError):
            fun7(10, 0)


if __name__ == '__main__':
    unittest.main()