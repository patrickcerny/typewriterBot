"""Command line interface for TypeWriterBot."""

from __future__ import annotations

import argparse
import logging
import os
from typing import Sequence

from .bot import (
    ERROR_INVALID_ARGUMENTS,
    create_driver,
    do_exercise,
    exit_with_message,
    goto_home_screen,
    login,
    next_lesson,
)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""

    parser = argparse.ArgumentParser(description="Automate Typewriter exercises")
    parser.add_argument(
        "--browser",
        choices=["f", "c", "e"],
        required=True,
        help="Browser to use: Firefox(f), Chrome(c), Edge(e)",
    )
    parser.add_argument(
        "--speed", type=int, required=True, help="Typing speed in characters per minute"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    login_parser = subparsers.add_parser("login", help="Log in and run exercises")
    login_parser.add_argument(
        "--times", type=int, default=1, help="Number of exercises to perform"
    )

    exercise_parser = subparsers.add_parser(
        "exercise", help="Run a single exercise from a URL"
    )
    exercise_parser.add_argument("url", help="Exercise URL")

    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    """Run the command line interface."""

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args(argv)

    driver = create_driver(args.browser)

    if args.command == "login":
        username = os.getenv("TWB_USERNAME")
        password = os.getenv("TWB_PASSWORD")
        if not username or not password:
            exit_with_message(True, "Environment variables TWB_USERNAME and TWB_PASSWORD are required")
        login(driver, username, password)
        for _ in range(args.times):
            next_lesson(driver)
            do_exercise(driver, args.speed)
            goto_home_screen(driver)
        exit_with_message(False, "Exercises completed")

    if args.command == "exercise":
        try:
            driver.get(args.url)
            driver.maximize_window()
        except Exception as exc:  # pragma: no cover - network errors
            exit_with_message(True, str(exc))
        do_exercise(driver, args.speed)
        exit_with_message(False, "Exercise completed")

    exit_with_message(True, ERROR_INVALID_ARGUMENTS)


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
