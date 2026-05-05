from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Optional

import sympy as sp

from .errors import EvaluationError, ParseError
from .parser import parse_equation, parse_math, split_equation

ASSIGNMENT_RE = re.compile(r"^\s*([A-Za-z][A-Za-z0-9_]*)\s*=\s*(.+?)\s*$")
SOLVE_RE = re.compile(r"^\s*solve\s+([A-Za-z][A-Za-z0-9_]*)\s*:\s*(.+?)\s*$", re.I)


@dataclass(frozen=True)
class CalcResult:
    kind: str
    expression: Optional[sp.Basic] = None
    simplified: Optional[sp.Basic] = None
    numeric: Optional[sp.Basic] = None
    variable: Optional[str] = None
    equation: Optional[sp.Equality] = None
    solutions: Optional[List[sp.Basic]] = None


class Calculator:
    def __init__(self, precision: int = 12) -> None:
        self.precision = precision
        self.variables: Dict[str, sp.Basic] = {}

    def clear(self) -> None:
        self.variables.clear()

    def evaluate(self, line: str) -> CalcResult:
        text = line.strip()
        if not text:
            raise ParseError("Enter an expression to evaluate.")

        solve_match = SOLVE_RE.match(text)
        if solve_match:
            return self._solve(solve_match.group(2), solve_match.group(1))

        assignment_match = ASSIGNMENT_RE.match(text)
        if assignment_match and not assignment_match.group(2).lstrip().startswith("="):
            name, raw_expr = assignment_match.groups()
            expr = parse_math(raw_expr, self.variables).expression
            simplified = sp.simplify(expr)
            self.variables[name] = simplified
            return CalcResult(
                kind="assignment",
                variable=name,
                expression=simplified,
                simplified=simplified,
                numeric=self._numeric_if_possible(simplified),
            )

        if "=" in text:
            return self._solve(text, None)

        expr = parse_math(text, self.variables).expression
        simplified = sp.simplify(expr)
        return CalcResult(
            kind="expression",
            expression=expr,
            simplified=simplified,
            numeric=self._numeric_if_possible(simplified),
        )

    def _solve(self, raw: str, variable_name: Optional[str]) -> CalcResult:
        try:
            if "=" in raw:
                equation = parse_equation(raw, self.variables)
            else:
                expr = parse_math(raw, self.variables).expression
                equation = sp.Eq(expr, 0)
        except ValueError as exc:
            raise ParseError(str(exc)) from exc

        symbol = self._solve_symbol(equation, variable_name)
        try:
            solutions = sp.solve(equation, symbol)
        except Exception as exc:
            raise EvaluationError(f"Could not solve for {symbol}.") from exc

        return CalcResult(
            kind="solve",
            equation=equation,
            variable=str(symbol),
            solutions=[sp.simplify(solution) for solution in solutions],
        )

    def _solve_symbol(self, equation: sp.Equality, variable_name: Optional[str]) -> sp.Symbol:
        if variable_name:
            return sp.Symbol(variable_name)

        symbols = sorted(equation.free_symbols, key=lambda item: item.name)
        if len(symbols) != 1:
            raise EvaluationError(
                "Equations without 'solve <var>:' must contain exactly one unknown."
            )
        return symbols[0]

    def _numeric_if_possible(self, expr: sp.Basic) -> Optional[sp.Basic]:
        if getattr(expr, "free_symbols", None):
            return None
        numeric = expr.evalf(self.precision)
        return numeric if numeric != expr else None

