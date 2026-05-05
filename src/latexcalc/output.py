from __future__ import annotations

from typing import Iterable

import sympy as sp
from rich.console import Console
from rich.text import Text

from .evaluator import CalcResult


def format_plain(result: CalcResult) -> str:
    if result.kind == "assignment":
        return f"{result.variable} = {result.simplified}"
    if result.kind == "solve":
        return _format_solutions(result.variable or "x", result.solutions or [])
    return str(result.simplified)


def format_latex(result: CalcResult) -> str:
    if result.kind == "assignment":
        return rf"{result.variable} = {sp.latex(result.simplified)}"
    if result.kind == "solve":
        solutions = result.solutions or []
        if not solutions:
            return r"\varnothing"
        return ", ".join(rf"{result.variable} = {sp.latex(solution)}" for solution in solutions)
    return sp.latex(result.simplified)


def print_result(console: Console, result: CalcResult, *, plain: bool = False, latex: bool = False) -> None:
    if plain:
        console.print(format_plain(result))
        return
    if latex:
        console.print(format_latex(result))
        return

    if result.kind == "assignment":
        console.print(Text(f"{result.variable} =", style="bold cyan"))
        console.print(sp.pretty(result.simplified))
    elif result.kind == "solve":
        console.print(Text(f"solve {result.variable}", style="bold cyan"))
        console.print(format_plain(result))
    else:
        console.print(sp.pretty(result.simplified))

    if result.numeric is not None and result.numeric != result.simplified:
        console.print(Text(f"≈ {result.numeric}", style="dim"))


def _format_solutions(variable: str, solutions: Iterable[sp.Basic]) -> str:
    values = list(solutions)
    if not values:
        return "no solutions"
    return ", ".join(f"{variable} = {solution}" for solution in values)

