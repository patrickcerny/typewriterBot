"""Core automation logic for TypeWriterBot."""

from __future__ import annotations

import logging
import sys
import time
from typing import Literal

from pynput.keyboard import Controller
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

keyboard = Controller()

ERROR_INVALID_ARGUMENTS = "Invalid arguments"


def exit_with_message(error: bool, message: str = "") -> None:
    """Log a message and exit the program.

    Args:
        error: Whether an error occurred.
        message: Message to log before exiting.
    """

    if error:
        logging.error("%s", message)
        sys.exit(1)
    if message:
        logging.info("%s", message)
    sys.exit(0)


def create_driver(browser: Literal["f", "c", "e"]) -> webdriver.Remote:
    """Create a Selenium driver for the chosen browser."""

    try:
        if browser == "f":
            return webdriver.Firefox(service=FirefoxService(executable_path="./driver/geckodriver"))
        if browser == "c":
            return webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        if browser == "e":
            return webdriver.Edge(service=EdgeService("./driver/msedgedriver"))
    except WebDriverException as exc:  # pragma: no cover - driver errors
        exit_with_message(True, str(exc))
    exit_with_message(True, ERROR_INVALID_ARGUMENTS)


def login(driver: webdriver.Remote, username: str, password: str) -> None:
    """Log in to the Typewriter website."""

    try:
        driver.get("https://at4.typewriter.at/index.php?r=site/index")
        driver.maximize_window()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "LoginForm_username"))
        )
        form_login_un = driver.find_element(By.ID, "LoginForm_username")
        form_login_pw = driver.find_element(By.ID, "LoginForm_pw")
        form_login_submit = driver.find_element(By.NAME, "yt0")
    except (WebDriverException, NoSuchElementException) as exc:  # pragma: no cover - network/element errors
        exit_with_message(True, str(exc))

    form_login_un.send_keys(username)
    form_login_pw.send_keys(password)
    form_login_submit.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "cockpitStartButton"))
    )


def next_lesson(driver: webdriver.Remote) -> None:
    """Open the next lesson."""

    try:
        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "cockpitStartButton"))
        )
        link.click()
    except (WebDriverException, NoSuchElementException) as exc:  # pragma: no cover - element errors
        exit_with_message(True, str(exc))


def do_exercise(driver: webdriver.Remote, speed: int) -> None:
    """Perform the typing exercise."""

    keyboard.press(Keys.ENTER)
    keyboard.release(Keys.ENTER)

    try:
        box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "text_todo_1"))
        )
    except (WebDriverException, NoSuchElementException) as exc:  # pragma: no cover - element errors
        exit_with_message(True, str(exc))

    keyboard.press(Keys.ENTER)
    keyboard.release(Keys.ENTER)

    current_char = box.find_element(By.TAG_NAME, "span").text
    keyboard.type(current_char)

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
    """Return to the user's home screen."""

    try:
        driver.get("https://at4.typewriter.at/index.php?r=user/overview")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cockpitStartButton"))
        )
    except WebDriverException as exc:  # pragma: no cover - network errors
        exit_with_message(True, str(exc))
