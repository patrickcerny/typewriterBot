import sys
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pynput.keyboard import Controller, Key
import keyboard
import time
import geckodriver_autoinstaller
from webdriverdownloader import GeckoDriverDownloader
from webdriverdownloader import ChromeDriverDownloader

keyboardpy = Controller()

errorList = [
    "Invalid Argument",
    "connection refused, check internet connection"
]


def Exit(Error, errorMessage):
    if Error:
        print("Error! something went wrong!")
        print("Error Message: " + str(errorMessage))

    print("Press any key to exit!")
    input()
    sys.exit(0)

# function for loggin into an account and starting the newest lesson
def Login():
    print("Hello User!\nThis is a warning! This application has to use your typetrainer username and password! " +
          "The credentials will not be saved in any way. They serve for login purpose only. " +
          "Do you want to continue) (y/n)")
    answer = input().strip().lower()

    if answer == "n":
        Exit(False, "")

    print("Please Enter your Username:")
    username = input()
    print("Please enter your Password")
    password = input()

    if answerBrowser == "f":
        driver = webdriver.Firefox()
    elif answerBrowser == "c":
        driver = webdriver.Chrome("driver\chromedriver.exe")
    elif answerBrowser == "e":
        driver = webdriver.Edge("driver\msedgedriver.exe")
    else:
        Exit(True, errorList[0])

    try:
      driver.get("https://at4.typewriter.at/index.php?r=site/index")
    except Exception as e:
      Exit(True, e)


    

    # login in homepage
    try:
      formLogin_un = driver.find_element_by_id("LoginForm_username")
      formLogin_pw = driver.find_element_by_id("LoginForm_pw")
      formLogin_submit = driver.find_element_by_name("yt0")
    
    # paste in user-credentials
      formLogin_un.send_keys(username)
      formLogin_pw.send_keys(password)
      formLogin_submit.click()
    except Exception as e:
      Exit(True, e)

    time.sleep(1)


    return driver

def NextLesson(driver):
  # opens link to next lesson
  linkToLesson = driver.find_element_by_class_name("cockpitStartButton")
  linkToLesson.click()

# function for doing an excercise on typewriter
def DoExcercise(driver):

    time.sleep(1)
    # gets first char of text
    try:
      currentChar = driver.find_element_by_id("actualLetter").text
    except Exception as e:
      Exit(True, e)
    
    # starts the lesson
    keyboardpy.press(Keys.ENTER)
    time.sleep(0.5)

    # types the first char again for update of #remainingText
    keyboardpy.press(currentChar)

    # gets remaining text + currentchar
    try:
      remainingText = driver.find_element_by_id("remainingText").text
      currentChar = driver.find_element_by_id("actualLetter").text
    except Exception as e:
      Exit(True, e)

    # types the 2nd char
    time.sleep(0.5)
    keyboardpy.press(currentChar)



    # types every char in the remaining Text
    for char in remainingText:
        keyboardpy.press(char)
        time.sleep(60/int(answerSpeed))

def GotoHomescreen():

  try:
    if answerBrowser == "f":
      driver = webdriver.Firefox()
    elif answerBrowser == "c":
      driver = webdriver.Chrome("driver\chromedriver.exe")
    elif answerBrowser == "e":
      driver = webdriver.Edge("driver\msedgedriver.exe")
    else:
      Exit(True, errorList[0])

    driver.get("https://at4.typewriter.at/index.php?r=user/overview")
    return driver  
  except Exception as e:
    Exit(True, e)

print(".")
print(".")
print(".")
print("TypeWriterBot by Patrick Cerny, Github: https://github.com/patrickcerny")
print(".")
print(".")
print(".")

# choosing of browser
print("What Browser do you use? (Firefox: F | Chrome: C | Edge: E)")
answerBrowser = input().strip().lower()
if answerBrowser != "e" and answerBrowser != "f" and answerBrowser != "c":
    Exit(True, errorList[0])

# assignment of typespeed 
print("What speed to you want to type in? (f. e. 300 => 300 chars / min - [It will always finish a bit less then the amount you type in!])")
try:
  answerSpeed = int(input())
except Exception as e:
  Exit(True, e)

# login or excercise
print("Do you want to login and do your next Exercise or just do a Excercise without login? (Login: L | Excerice: E)")
answer = input().strip().lower()
if answer == "l":
  print("How many excercises do you want to do? (1 to How-Many-You-Want)")
  try:
    timesExcercise = int(input())
  except Exception as e:
    Exit(True, e)

  driver = Login()
  for i in range(timesExcercise):
    NextLesson(driver)
    DoExcercise(driver)
    


elif answer == "e":
    print("Please provide the URL of the excercise:")
    url = input()
    try:
      if answerBrowser == "f":
          driver = webdriver.Firefox()
      elif answerBrowser == "c":
          driver = webdriver.Chrome(".\driver\chromedriver.exe")
      elif answerBrowser == "e":
          driver = webdriver.Edge(".\driver\msedgedriver.exe")
    except Exception as e:
      Exit(True, e)
    
    try:
      driver.get(url)
    except Exception as e:
      Exit(True, e)
    
    DoExcercise(driver)
else:
  Exit(True, errorList[0])

