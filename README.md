# LaTeX-Aware CLI Calculator

`calc` is a terminal scratchpad that accepts normal math and common LaTeX math.
It can run as an interactive REPL or evaluate a single expression from your
shell.

## Install

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
```

After activating the virtual environment, the `calc` command is available in
that terminal session.

## One-Shot Use

Use single quotes around LaTeX expressions so the shell leaves backslashes
alone:

```sh
calc --plain '\frac{2}{3} + \sqrt{16}'
calc --plain 'solve x: x^2 = 4'
calc --latex 'x^2'
```

Useful flags:

```sh
calc --plain '1 / 3'
calc --latex '\frac{1}{2}'
calc --precision 20 '1 / 3'
```

## Interactive REPL

Start the REPL with:

```sh
calc
```

The interactive REPL supports session variables, command history, completions,
and commands like `:help`, `:vars`, `:clear`, and `:quit`.

Example session:

```text
calc> x = 12
calc> y = \frac{x}{3}
calc> :vars
calc> solve z: z^2 = 4
calc> :quit
```

Function names need arguments. For example, use `ln(2)`, `sqrt(4)`, or
`\sqrt{4}` rather than typing only `ln` or `sqrt`.

## Supported Input

- Normal math: `2x + sqrt(4)`, `x^2`, `ln(2)`
- Common LaTeX: `\frac{1}{2}`, `\sqrt{16}`, `\pi`
- Pasted math delimiters: `$\frac{1}{2}$`, `\[\frac{1}{2}\]`
- Session assignments in the REPL: `x = 12`
- Simple equations: `x^2 = 4` or `solve x: x^2 - 4`

SymPy's LaTeX parser is experimental, so some valid-looking TeX notation may
not parse yet. When that happens, `calc` reports a user-facing parse error
instead of a Python traceback.

## Development Commands

```sh
. .venv/bin/activate
pytest
```
