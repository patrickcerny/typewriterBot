import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from pynput.keyboard import Controller
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

keyboardpy = Controller()

errorList = [
    "Invalid Arguments",
    "Connection refused, check internet connection"
]

def Exit(Error, errorMessage):
    if Error:
        print("Error! Something went wrong!")
        print("Error Message: " + errorMessage)
    print("Press Enter to exit.")
    input()
    sys.exit(0)

def Login():
    print(
        "Hello User!\nThis is a warning! This application has to use your typetrainer username and password! "
        "The credentials will not be saved in any way. They serve for login purposes only.\n"
        "Do you want to continue? (y/n)"
    )
    answer = input().strip().lower()

    if answer == "n":
        Exit(False, "")

    print("Please Enter your Username:")
    username = input().strip()
    print("Please Enter your Password:")
    password = input().strip()

    if answerBrowser == "f":
        driver = webdriver.Firefox(service=FirefoxService(executable_path="./driver/geckodriver"))
    elif answerBrowser == "c":
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    elif answerBrowser == "e":
        driver = webdriver.Edge(service=EdgeService("./driver/msedgedriver"))
    else:
        Exit(True, errorList[0])

    try:
        driver.get("https://at4.typewriter.at/index.php?r=site/index")
        driver.maximize_window()
        time.sleep(1)
    except Exception as e:
        Exit(True, str(e))

    try:
        formLogin_un = driver.find_element(By.ID, "LoginForm_username")
        formLogin_pw = driver.find_element(By.ID, "LoginForm_pw")
        formLogin_submit = driver.find_element(By.NAME, "yt0")
    except Exception as e:
        Exit(True, str(e))

    time.sleep(1)   

    formLogin_un.send_keys(username)
    formLogin_pw.send_keys(password)
    formLogin_submit.click()

    time.sleep(1)
    return driver

def NextLesson(driver):
    time.sleep(1)
    try:
        linkToLesson = driver.find_element(By.CLASS_NAME, "cockpitStartButton")
        linkToLesson.click()
    except Exception as e:
        Exit(True, str(e))

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

    amountRemaining = driver.find_element(By.ID, "amountRemaining").text
    remainingInt = int(amountRemaining)

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

    driver = Login()
    for _ in range(timesExercise):
        NextLesson(driver)
        DoExercise(driver)
        time.sleep(1)
        GotoHomeScreen(driver)

elif answer == "e":
    print("Please provide the URL of the exercise:")
    url = input().strip()
    try:
        if answerBrowser == "f":
            driver = webdriver.Firefox(service=FirefoxService(executable_path="./driver/geckodriver"))
        elif answerBrowser == "c":
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        elif answerBrowser == "e":
            driver = webdriver.Edge(service=EdgeService("./driver/msedgedriver"))
        else:
            Exit(True, errorList[0])

        driver.get(url)
        driver.maximize_window()
    except Exception as e:
        Exit(True, str(e))

    DoExercise(driver)
else:
    Exit(True, errorList[0])

print("Thank you for using my bot! If you have any feedback, please contact me on GitHub: https://github.com/patrickcerny")
