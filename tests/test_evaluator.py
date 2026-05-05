import sympy as sp

from latexcalc.evaluator import Calculator


def test_evaluates_and_simplifies_expression():
    calc = Calculator()
    result = calc.evaluate(r"\frac{2}{3} + \sqrt{16}")
    assert result.simplified == sp.Rational(14, 3)
    assert result.numeric is not None


def test_session_assignment_and_substitution():
    calc = Calculator()
    assigned = calc.evaluate("x = 12")
    result = calc.evaluate(r"y = \frac{x}{3}")
    assert assigned.simplified == 12
    assert result.variable == "y"
    assert calc.variables["y"] == 4


def test_clear_removes_session_variables():
    calc = Calculator()
    calc.evaluate("x = 12")
    calc.clear()
    result = calc.evaluate("x + 1")
    assert result.simplified == sp.Symbol("x") + 1


def test_solves_single_unknown_equation():
    calc = Calculator()
    result = calc.evaluate("x^2 = 4")
    assert result.variable == "x"
    assert result.solutions == [-2, 2]


def test_solves_explicit_variable_expression():
    calc = Calculator()
    result = calc.evaluate("solve x: x^2 - 4")
    assert result.variable == "x"
    assert result.solutions == [-2, 2]

