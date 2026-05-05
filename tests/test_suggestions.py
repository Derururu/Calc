from prompt_toolkit.document import Document

from latexcalc.evaluator import Calculator
from latexcalc.suggestions import CalcCompleter


def completions_for(text, calculator=None):
    completer = CalcCompleter(calculator or Calculator())
    return list(completer.get_completions(Document(text), None))


def test_latex_command_completion():
    completions = completions_for(r"\fr")
    assert any(item.text == r"\frac{}{}" for item in completions)


def test_variable_completion_from_session_state():
    calc = Calculator()
    calc.evaluate("radius = 4")
    completions = completions_for("rad", calc)
    assert any(item.text == "radius" for item in completions)


def test_repl_command_completion():
    completions = completions_for(":v")
    assert any(item.text == ":vars" for item in completions)

