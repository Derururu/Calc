from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict

import sympy as sp
from sympy.parsing.latex import LaTeXParsingError, parse_latex
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

from .errors import ParseError

TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)

LATEX_COMMAND_RE = re.compile(r"\\[A-Za-z]+")
DISPLAY_DELIMITERS = (
    (r"\[", r"\]"),
    (r"\(", r"\)"),
    ("$$", "$$"),
    ("$", "$"),
)


@dataclass(frozen=True)
class ParsedInput:
    source: str
    normalized: str
    expression: sp.Basic
    parser: str


def strip_math_delimiters(text: str) -> str:
    value = text.strip()
    changed = True
    while changed:
        changed = False
        for opening, closing in DISPLAY_DELIMITERS:
            if value.startswith(opening) and value.endswith(closing):
                value = value[len(opening) : len(value) - len(closing)].strip()
                changed = True
                break
    return value


def looks_like_latex(text: str) -> bool:
    return bool(LATEX_COMMAND_RE.search(text))


def parse_math(text: str, variables: Dict[str, sp.Basic] | None = None) -> ParsedInput:
    normalized = strip_math_delimiters(text)
    if not normalized:
        raise ParseError("Enter an expression to evaluate.")

    parser_name = "latex" if looks_like_latex(normalized) else "sympy"
    try:
        if parser_name == "latex":
            expr = parse_latex(normalized, strict=True)
        else:
            expr = parse_expr(normalized, transformations=TRANSFORMATIONS, evaluate=True)
    except (LaTeXParsingError, SyntaxError, TypeError, ValueError) as exc:
        raise ParseError(f"Could not parse expression: {normalized}") from exc

    if not isinstance(expr, sp.Basic):
        raise ParseError(
            f"Could not parse expression: {normalized}. "
            "Function names need arguments, for example ln(2)."
        )
    expr = sp.simplify(normalize_constants(expr))
    if variables:
        expr = expr.subs(variables)
    return ParsedInput(source=text, normalized=normalized, expression=expr, parser=parser_name)


def parse_equation(text: str, variables: Dict[str, sp.Basic] | None = None) -> sp.Equality:
    normalized = strip_math_delimiters(text)
    left, right = split_equation(normalized)
    left_expr = parse_math(left, variables).expression
    right_expr = parse_math(right, variables).expression
    return sp.Eq(left_expr, right_expr)


def split_equation(text: str) -> tuple[str, str]:
    if text.count("=") != 1:
        raise ParseError("Expected one equation sign.")
    left, right = text.split("=", 1)
    if not left.strip() or not right.strip():
        raise ParseError("Equations need expressions on both sides of '='.")
    return left, right


def normalize_constants(expr: sp.Basic) -> sp.Basic:
    replacements = {
        sp.Symbol("pi"): sp.pi,
        sp.Symbol("Pi"): sp.pi,
        sp.Symbol("infty"): sp.oo,
    }
    return expr.xreplace(replacements)
