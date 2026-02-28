# GitHub Lab 1 - Calculator with CI/CD

This lab is based on [MLOps GitHub Lab 1](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Github_Labs/Lab1) by Professor Ramin Mohammadi (Northeastern University).

## Overview

A simple Python calculator project demonstrating:
- Project structure and virtual environments
- Unit testing with **Pytest** and **Unittest**
- CI/CD automation with **GitHub Actions**

## Project Structure

```
Lab1/
├── data/
│   └── __init__.py
├── src/
│   ├── __init__.py
│   └── calculator.py
├── test/
│   ├── __init__.py
│   ├── test_pytest.py
│   └── test_unittest.py
├── .github/
│   └── workflows/
│       ├── pytest_action.yml
│       └── unittest_action.yml
├── .gitignore
├── requirements.txt
└── README.md
```

## Changes Made (From Original Lab)

### 1. Added New Calculator Functions

The original `calculator.py` had 4 functions. I added 3 more:

| Function | Operation       | Description                                      |
|----------|----------------|--------------------------------------------------|
| `fun1`   | Addition        | Returns `x + y` *(original)*                     |
| `fun2`   | Subtraction     | Returns `x - y` *(original)*                     |
| `fun3`   | Multiplication  | Returns `x * y` *(original)*                     |
| `fun4`   | Combined        | Returns sum of fun1, fun2, fun3 *(original)*     |
| `fun5`   | Division        | Returns `x / y` with zero-division check **NEW** |
| `fun6`   | Power           | Returns `x ** y` **NEW**                         |
| `fun7`   | Modulo          | Returns `x % y` with zero-division check **NEW** |

### 2. Added Error Handling

- `fun5` (division) raises `ValueError` when dividing by zero
- `fun7` (modulo) raises `ValueError` when modulo by zero

### 3. Added New Test Cases

Extended both `test_pytest.py` and `test_unittest.py` with:

- **test_fun5** — Tests normal division (positive, negative, float results)
- **test_fun5_divide_by_zero** — Verifies `ValueError` is raised
- **test_fun6** — Tests power with positive, zero, and negative exponents
- **test_fun7** — Tests normal modulo operations
- **test_fun7_mod_by_zero** — Verifies `ValueError` is raised

Total tests: **4 original + 5 new = 9 tests** per test file

## Setup & Usage

### 1. Clone the repository
```bash
git clone <your_repo_url>
cd github_lab1
```

### 2. Create and activate virtual environment
```bash
python -m venv github_lab1_env

# Mac/Linux
source github_lab1_env/bin/activate

# Windows
github_lab1_env\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run tests
```bash
# Pytest
pytest test/test_pytest.py

# Unittest
python -m unittest test.test_unittest
```

## CI/CD

GitHub Actions automatically runs both Pytest and Unittest workflows on every push or pull request to `main`.

- **pytest_action.yml** — Runs pytest and uploads XML report as artifact
- **unittest_action.yml** — Runs unittest suite
