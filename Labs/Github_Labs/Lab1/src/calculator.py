"""
calculator.py - Basic and extended arithmetic operations
"""


def fun1(x, y):
    """Addition: returns x + y"""
    return x + y


def fun2(x, y):
    """Subtraction: returns x - y"""
    return x - y


def fun3(x, y):
    """Multiplication: returns x * y"""
    return x * y


def fun4(x, y):
    """Combines results of fun1, fun2, and fun3 and returns their sum"""
    result = fun1(x, y) + fun2(x, y) + fun3(x, y)
    return result


def fun5(x, y):
    """Division: returns x / y. Raises ValueError if y is 0."""
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y


def fun6(x, y):
    """Power: returns x raised to the power of y"""
    return x ** y


def fun7(x, y):
    """Modulo: returns x % y. Raises ValueError if y is 0."""
    if y == 0:
        raise ValueError("Cannot perform modulo by zero")
    return x % y