import sys


def exit_with_message(error: bool, error_message: str = "") -> None:
    """Print an optional message and exit with an appropriate status code.

    When *error* is ``True`` the message, if provided, is written to stderr and
    the process exits with status code ``1``.  For non-error exits the message is
    written to stdout and the process terminates with status code ``0``.
    """
    if error_message:
        stream = sys.stderr if error else sys.stdout
        print(error_message, file=stream)
    sys.exit(1 if error else 0)
