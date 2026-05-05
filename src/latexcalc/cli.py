from __future__ import annotations

import argparse
import sys
from pathlib import Path

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from rich.console import Console

from .errors import CalculatorError
from .evaluator import Calculator
from .output import print_result
from .suggestions import CalcCompleter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="calc",
        description="Evaluate normal math and common LaTeX math from the terminal.",
    )
    parser.add_argument("expression", nargs="*", help="Expression to evaluate.")
    parser.add_argument("--latex", action="store_true", help="Print result as LaTeX.")
    parser.add_argument("--plain", action="store_true", help="Print a plain text result.")
    parser.add_argument(
        "--precision",
        type=int,
        default=12,
        help="Decimal precision for numeric approximations.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    console = Console(stderr=False)
    calculator = Calculator(precision=args.precision)
    if args.expression:
        expression = " ".join(args.expression)
        return run_one_shot(calculator, expression, console, plain=args.plain, latex=args.latex)
    return run_repl(calculator, console)


def run_one_shot(
    calculator: Calculator,
    expression: str,
    console: Console,
    *,
    plain: bool = False,
    latex: bool = False,
) -> int:
    try:
        result = calculator.evaluate(expression)
    except CalculatorError as exc:
        Console(stderr=True).print(f"error: {exc}", style="bold red")
        return 1
    print_result(console, result, plain=plain, latex=latex)
    return 0


def run_repl(calculator: Calculator, console: Console) -> int:
    history_path = Path.home() / ".calc_history"
    session = PromptSession(
        history=FileHistory(str(history_path)),
        completer=CalcCompleter(calculator),
        auto_suggest=AutoSuggestFromHistory(),
        complete_while_typing=True,
    )
    console.print("LaTeX-aware calc. Type :help for commands.")
    while True:
        try:
            line = session.prompt("calc> ")
        except (EOFError, KeyboardInterrupt):
            console.print()
            return 0

        stripped = line.strip()
        if not stripped:
            continue
        if stripped in {":quit", ":exit"}:
            return 0
        if stripped == ":help":
            print_help(console)
            continue
        if stripped == ":vars":
            print_variables(console, calculator)
            continue
        if stripped == ":clear":
            calculator.clear()
            console.print("cleared")
            continue

        try:
            result = calculator.evaluate(stripped)
        except CalculatorError as exc:
            console.print(f"error: {exc}", style="bold red")
            continue
        print_result(console, result)


def print_help(console: Console) -> None:
    console.print(
        "\n".join(
            [
                "Examples:",
                r"  \frac{1}{2} + 2x",
                "  x = 12",
                r"  y = \frac{x}{3}",
                "  x^2 = 4",
                "  solve x: x^2 - 4",
                "",
                "Commands: :vars, :clear, :quit",
            ]
        )
    )


def print_variables(console: Console, calculator: Calculator) -> None:
    if not calculator.variables:
        console.print("no variables")
        return
    for name, value in sorted(calculator.variables.items()):
        console.print(f"{name} = {value}")


if __name__ == "__main__":
    sys.exit(main())
