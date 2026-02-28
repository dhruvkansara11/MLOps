"""
test_pytest.py - Pytest tests for calculator.py
"""

import sys
import os
import pytest

# Add the parent directory to path so we can import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.calculator import fun1, fun2, fun3, fun4, fun5, fun6, fun7


# --- Original tests ---

def test_fun1():
    """Test addition function"""
    assert fun1(2, 3) == 5
    assert fun1(-1, 1) == 0
    assert fun1(0, 0) == 0


def test_fun2():
    """Test subtraction function"""
    assert fun2(5, 3) == 2
    assert fun2(0, 5) == -5
    assert fun2(10, 10) == 0


def test_fun3():
    """Test multiplication function"""
    assert fun3(3, 4) == 12
    assert fun3(-2, 3) == -6
    assert fun3(0, 100) == 0


def test_fun4():
    """Test combined function"""
    # fun4(2,3) = fun1(2,3) + fun2(2,3) + fun3(2,3)
    #           = (2+3) + (2-3) + (2*3)
    #           = 5 + (-1) + 6 = 10
    assert fun4(2, 3) == 10
    assert fun4(0, 0) == 0


# --- New tests for added functions ---

def test_fun5():
    """Test division function"""
    assert fun5(10, 2) == 5.0
    assert fun5(-9, 3) == -3.0
    assert fun5(7, 2) == 3.5


def test_fun5_divide_by_zero():
    """Test division raises ValueError on divide by zero"""
    with pytest.raises(ValueError):
        fun5(10, 0)


def test_fun6():
    """Test power function"""
    assert fun6(2, 3) == 8
    assert fun6(5, 0) == 1
    assert fun6(3, 2) == 9
    assert fun6(2, -1) == 0.5


def test_fun7():
    """Test modulo function"""
    assert fun7(10, 3) == 1
    assert fun7(20, 5) == 0
    assert fun7(7, 4) == 3


def test_fun7_mod_by_zero():
    """Test modulo raises ValueError on mod by zero"""
    with pytest.raises(ValueError):
        fun7(10, 0)