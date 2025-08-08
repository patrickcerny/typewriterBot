import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from pynput.keyboard import Controller

keyboard = Controller()

ERROR_INVALID_ARGUMENTS = "Invalid Arguments"


def exit_with_message(error: bool, message: str = "") -> None:
    """Exit the program after printing a message."""
    if error:
        print("Error! Something went wrong!")
        print("Error Message: " + message)
    input("Press Enter to exit.")
    sys.exit(0)


def create_driver(browser: str) -> webdriver.Remote:
    """Create a Selenium driver for the chosen browser."""
    if browser == "f":
        return webdriver.Firefox(service=FirefoxService(executable_path="./driver/geckodriver"))
    if browser == "c":
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    if browser == "e":
        return webdriver.Edge(service=EdgeService("./driver/msedgedriver"))
    exit_with_message(True, ERROR_INVALID_ARGUMENTS)


def login(driver: webdriver.Remote, username: str, password: str) -> None:
    try:
        driver.get("https://at4.typewriter.at/index.php?r=site/index")
        driver.maximize_window()
        time.sleep(1)
    except Exception as e:  # pragma: no cover - network errors
        exit_with_message(True, str(e))

    try:
        form_login_un = driver.find_element(By.ID, "LoginForm_username")
        form_login_pw = driver.find_element(By.ID, "LoginForm_pw")
        form_login_submit = driver.find_element(By.NAME, "yt0")
    except Exception as e:  # pragma: no cover - element errors
        exit_with_message(True, str(e))

    time.sleep(1)
    form_login_un.send_keys(username)
    form_login_pw.send_keys(password)
    form_login_submit.click()
    time.sleep(1)


def next_lesson(driver: webdriver.Remote) -> None:
    time.sleep(1)
    try:
        link = driver.find_element(By.CLASS_NAME, "cockpitStartButton")
        link.click()
    except Exception as e:  # pragma: no cover - element errors
        exit_with_message(True, str(e))


def do_exercise(driver: webdriver.Remote, speed: int) -> None:
    keyboard.press(Keys.ENTER)
    keyboard.release(Keys.ENTER)
    time.sleep(1)

    try:
        box = driver.find_element(By.ID, "text_todo_1")
    except Exception as e:  # pragma: no cover - element errors
        exit_with_message(True, str(e))

    # remove checkbox
    keyboard.press(Keys.ENTER)
    keyboard.release(Keys.ENTER)
    time.sleep(2.5)

    # find first key
    current_char = box.find_element(By.TAG_NAME, "span").text
    keyboard.type(current_char)
    time.sleep(2.5)

    amount_remaining = driver.find_element(By.ID, "amountRemaining").text
    remaining = int(amount_remaining)

    while remaining > 0:
        box = driver.find_element(By.ID, "text_todo_1")
        current_char = box.find_element(By.TAG_NAME, "span").text
        keyboard.type(current_char)
        time.sleep(60 / speed)
        amount_remaining = driver.find_element(By.ID, "amountRemaining").text
        remaining = int(amount_remaining)


def goto_home_screen(driver: webdriver.Remote) -> None:
    try:
        driver.get("https://at4.typewriter.at/index.php?r=user/overview")
        time.sleep(5)
    except Exception as e:  # pragma: no cover - network errors
        exit_with_message(True, str(e))
