import sys


def exit_with_message(error: bool, error_message: str = "") -> None:
    """Print an optional error message and exit.

    If *error* is truthy, the message is treated as an error and the process
    terminates with a status code of ``1``. Otherwise the process exits with
    status code ``0``. The previous implementation waited for user input before
    exiting which caused automated environments to hang; that behaviour has been
    removed.
    """
    if error:
        print("Error! Something went wrong!")
        if error_message:
            print("Error Message: " + error_message)
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    exit_with_message(True, "This module is not intended to be executed directly.")
