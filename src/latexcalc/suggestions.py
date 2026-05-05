from __future__ import annotations

import re
from typing import Iterable

from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document

LATEX_SNIPPETS = {
    r"\frac": r"\frac{}{}",
    r"\sqrt": r"\sqrt{}",
    r"\sin": r"\sin",
    r"\cos": r"\cos",
    r"\tan": r"\tan",
    r"\log": r"\log",
    r"\ln": r"\ln",
    r"\pi": r"\pi",
    r"\alpha": r"\alpha",
    r"\beta": r"\beta",
    r"\gamma": r"\gamma",
    r"\theta": r"\theta",
    r"\infty": r"\infty",
}

FUNCTIONS = (
    "sqrt",
    "sin",
    "cos",
    "tan",
    "log",
    "ln",
    "exp",
    "simplify",
    "solve",
)

COMMANDS = (":help", ":vars", ":clear", ":quit")
WORD_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*$")
LATEX_FRAGMENT_RE = re.compile(r"\\[A-Za-z]*$")


class CalcCompleter(Completer):
    def __init__(self, calculator) -> None:
        self.calculator = calculator

    def get_completions(self, document: Document, complete_event) -> Iterable[Completion]:
        text = document.text_before_cursor
        if text.startswith(":"):
            yield from self._complete_from(COMMANDS, text)
            return

        latex_match = LATEX_FRAGMENT_RE.search(text)
        if latex_match:
            fragment = latex_match.group(0)
            for command, snippet in LATEX_SNIPPETS.items():
                if command.startswith(fragment):
                    yield Completion(
                        snippet,
                        start_position=-len(fragment),
                        display=command,
                        display_meta="LaTeX",
                    )
            return

        word_match = WORD_RE.search(text)
        if not word_match:
            return
        fragment = word_match.group(0)
        words = list(FUNCTIONS) + sorted(self.calculator.variables)
        for word in words:
            if word.startswith(fragment) and word != fragment:
                meta = "variable" if word in self.calculator.variables else "function"
                suffix = "()" if meta == "function" and word != "solve" else ""
                yield Completion(
                    f"{word}{suffix}",
                    start_position=-len(fragment),
                    display=word,
                    display_meta=meta,
                )

    def _complete_from(self, options: Iterable[str], fragment: str) -> Iterable[Completion]:
        for option in options:
            if option.startswith(fragment):
                yield Completion(option, start_position=-len(fragment), display=option)

