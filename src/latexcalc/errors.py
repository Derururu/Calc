class CalculatorError(Exception):
    """Base exception for user-facing calculator errors."""


class ParseError(CalculatorError):
    """Raised when an expression cannot be parsed."""


class EvaluationError(CalculatorError):
    """Raised when a parsed expression cannot be evaluated."""

