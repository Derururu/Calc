# LaTeX-Aware CLI Calculator

`calc` is a terminal scratchpad that accepts normal math and common LaTeX math.

```sh
calc "\\frac{1}{2} + 2x"
calc "solve x: x^2 = 4"
calc
```

The interactive REPL supports session variables, command history, completions,
and commands like `:help`, `:vars`, `:clear`, and `:quit`.

## Development

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

