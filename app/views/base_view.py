"""
base_view.py — Common console output helpers.
Console output only: no input(), no business logic.
"""

SEPARATOR = "-" * 40


def print_separator() -> None:
    """Print a horizontal separator line."""
    print(SEPARATOR)


def print_header(title: str) -> None:
    """Print a section header with separator lines above and below the title."""
    print_separator()
    print(title)
    print_separator()


def print_error(message: str) -> None:
    """Print an error message with a visible [오류] prefix."""
    print(f"[오류] {message}")


def print_success(message: str) -> None:
    """Print a success message with a visible [성공] prefix."""
    print(f"[성공] {message}")
