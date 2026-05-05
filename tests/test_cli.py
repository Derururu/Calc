from rich.console import Console

from latexcalc.cli import main, run_one_shot
from latexcalc.evaluator import Calculator


def test_one_shot_plain_output(capsys):
    code = main(["--plain", r"\frac{1}{2} + \frac{1}{2}"])
    captured = capsys.readouterr()
    assert code == 0
    assert captured.out.strip() == "1"


def test_one_shot_latex_output(capsys):
    code = main(["--latex", "x^2"])
    captured = capsys.readouterr()
    assert code == 0
    assert captured.out.strip() == "x^{2}"


def test_one_shot_error_returns_nonzero(capsys):
    console = Console()
    code = run_one_shot(Calculator(), "x -", console)
    captured = capsys.readouterr()
    assert code == 1
    assert "error:" in captured.err


def test_bare_function_error_returns_nonzero_without_traceback(capsys):
    code = main(["--plain", "ln"])
    captured = capsys.readouterr()
    assert code == 1
    assert "Function names need arguments" in captured.err
    assert "Traceback" not in captured.err
