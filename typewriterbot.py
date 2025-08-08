import time

from bot import (
    ERROR_INVALID_ARGUMENTS,
    create_driver,
    do_exercise,
    exit_with_message,
    goto_home_screen,
    login,
    next_lesson,
)


def main() -> None:
    print("TypeWriterBot by Patrick Cerny, Github: https://github.com/patrickcerny\n")

    browser = input("What browser do you use? (Firefox: F | Chrome: C | Edge: E)\n").strip().lower()
    if browser not in ["f", "c", "e"]:
        exit_with_message(True, ERROR_INVALID_ARGUMENTS)

    action = input(
        "Do you want to log in and do your next exercise, or just do an exercise without login? (Login: L | Exercise: E)\n"
    ).strip().lower()

    try:
        speed = int(input("What speed do you want to type in? (e.g., 300 => 300 chars/min)\n").strip())
    except Exception as e:  # pragma: no cover - invalid input
        exit_with_message(True, str(e))

    if action == "l":
        try:
            times = int(input("How many exercises do you want to do? (1 or more)\n").strip())
        except Exception as e:
            exit_with_message(True, str(e))

        print(
            "Hello User!\nThis is a warning! This application has to use your typetrainer username and password! "
            "The credentials will not be saved in any way. They serve for login purposes only.\n"
            "Do you want to continue? (y/n)"
        )
        if input().strip().lower() == "n":
            exit_with_message(False)

        username = input("Please Enter your Username:\n").strip()
        password = input("Please Enter your Password:\n").strip()

        driver = create_driver(browser)
        login(driver, username, password)
        for _ in range(times):
            next_lesson(driver)
            do_exercise(driver, speed)
            time.sleep(1)
            goto_home_screen(driver)

    elif action == "e":
        url = input("Please provide the URL of the exercise:\n").strip()
        driver = create_driver(browser)
        try:
            driver.get(url)
            driver.maximize_window()
        except Exception as e:  # pragma: no cover - network errors
            exit_with_message(True, str(e))
        do_exercise(driver, speed)
    else:
        exit_with_message(True, ERROR_INVALID_ARGUMENTS)

    print(
        "Thank you for using my bot! If you have any feedback, please contact me on GitHub: https://github.com/patrickcerny"
    )


if __name__ == "__main__":
    main()
