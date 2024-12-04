import time

#selenium imports

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.service import Service


#keyboard input
from pynput.keyboard import Controller

#own imports
from files.errors import errorList
from files.functions import Exit
from files.functions import GetChromeDriver
from files.functions import NextLesson
from files.functions import LoginUser


keyboardpy = Controller()

def DoExercise(driver):
    keyboardpy.press(Keys.ENTER)
    time.sleep(1)
    try:
        box = driver.find_element(By.ID, "text_todo_1")
        currentChar = box.find_element(By.TAG_NAME, "span").text
    except Exception as e:
        Exit(True, str(e))

    # remove checkbox
    keyboardpy.press(Keys.ENTER)
    time.sleep(2.5)
    
    #find first key
    currentChar = box.find_element(By.TAG_NAME, "span").text
    keyboardpy.press(currentChar)
    time.sleep(2.5)

    amountRemaining: int = 0

    #try to find the remaining inputs after the first input
    try:
        amountRemaining = driver.find_element(By.ID, "amountRemaining").text
        remainingInt = int(amountRemaining)
    except Exception as e:
        Exit(True, str(e))

    while remainingInt > 0:
        # Locate the input box
        box = driver.find_element(By.ID, "text_todo_1")
        # Get the current character from the span inside the box
        currentChar = box.find_element(By.TAG_NAME, "span").text
        # Simulate typing the current character
        keyboardpy.press(currentChar)
        time.sleep(60 / int(answerSpeed))
        # Update the remaining count
        amountRemaining = driver.find_element(By.ID, "amountRemaining").text
        remainingInt = int(amountRemaining)

def GotoHomeScreen(driver):
    try:
        driver.get("https://at4.typewriter.at/index.php?r=user/overview")
        time.sleep(5)
    except Exception as e:
        Exit(True, str(e))

print("TypeWriterBot by Patrick Cerny, Github: https://github.com/patrickcerny\n")

print("What browser do you use? (Firefox: F | Chrome: C | Edge: E)")
answerBrowser = input().strip().lower()
if answerBrowser not in ["f", "c", "e"]:
    Exit(True, errorList[0])

print("Do you want to log in and do your next exercise, or just do an exercise without login? (Login: L | Exercise: E)")
answer = input().strip().lower()

print("What speed do you want to type in? (e.g., 300 => 300 chars/min)")
try:
    answerSpeed = int(input().strip())
except Exception as e:
    Exit(True, str(e))

if answer == "l":
    print("How many exercises do you want to do? (1 or more)")
    try:
        timesExercise = int(input().strip())
    except Exception as e:
        Exit(True, str(e))

    driver = LoginUser()
    for _ in range(timesExercise):
        NextLesson(driver)
        DoExercise(driver)
        time.sleep(1)
        GotoHomeScreen(driver)

elif answer == "e":
    print("Please provide the URL of the exercise:")
    url = input().strip()
    driver = GetChromeDriver();

    driver.get(url)
    driver.maximize_window()

    DoExercise(driver)
else:
    Exit(True, errorList[0])

print("Thank you for using my bot! If you have any feedback, please contact me on GitHub: https://github.com/patrickcerny")
