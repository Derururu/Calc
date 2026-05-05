import pytest
import sympy as sp

from latexcalc.errors import ParseError
from latexcalc.parser import parse_math, strip_math_delimiters


def test_parses_normal_math_with_implicit_multiplication():
    parsed = parse_math("2x + sqrt(4)")
    assert parsed.expression == 2 * sp.Symbol("x") + 2


def test_parses_latex_fraction():
    parsed = parse_math(r"\frac{1}{2}")
    assert parsed.expression == sp.Rational(1, 2)


def test_strips_common_math_delimiters():
    assert strip_math_delimiters(r"$\frac{1}{2}$") == r"\frac{1}{2}"
    assert strip_math_delimiters(r"\[\frac{1}{2}\]") == r"\frac{1}{2}"


def test_parses_latex_constant_pi_as_number():
    parsed = parse_math(r"\pi")
    assert parsed.expression == sp.pi


def test_malformed_input_has_clear_parse_error():
    with pytest.raises(ParseError, match="Could not parse expression"):
        parse_math("x -")


def test_bare_function_name_has_clear_parse_error():
    with pytest.raises(ParseError, match="Function names need arguments"):
        parse_math("ln")


def test_parses_function_with_arguments():
    parsed = parse_math("ln(2)")
    assert parsed.expression == sp.log(2)
