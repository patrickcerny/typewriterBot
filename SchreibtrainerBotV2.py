import sys
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pynput.keyboard import Controller, Key
import keyboard
import time
import geckodriver_autoinstaller
from webdriverdownloader import GeckoDriverDownloader

#automatic Gecko Installer
gdd = GeckoDriverDownloader()
gdd.download_and_install()


keyboardpy = Controller()

#function for loggin into an account and starting the newest lesson
def Login():
  print("Hello User!\nThis is a warning! This application has to use your typetrainer username and password! "+
    "The credentials will not be saved in any way. They serve for login purpose only. " +
    "Do you want to continue) (y/n)")
  answer = input().strip().lower()

  if answer == "n":
      sys.exit()
  



  print("Please Enter your Username:")
  username = input()
  print("Please enter your Password")
  password = input()

  if answerBrowser == "f":
    driver = webdriver.Firefox()
  elif answerBrowser == "c":
    driver = webdriver.Chrome()
  elif answerBrowser == "e":
    driver = webdriver.Edge() 
    
  driver.get("https://at4.typewriter.at/index.php?r=site/index")


  #login in homepage
  formLogin_un = driver.find_element_by_id("LoginForm_username")
  formLogin_pw = driver.find_element_by_id("LoginForm_pw")
  formLogin_submit = driver.find_element_by_name("yt0")

  formLogin_un.send_keys(username)
  formLogin_pw.send_keys(password)
  formLogin_submit.click()

  #open link to next lesson
  linkToLesson = driver.find_element_by_class_name("cockpitStartButton")
  linkToLesson.click()
  return driver

#function for doing an excercise on typewriter
def DoExcercise(driver):

  #gets first char of text
  currentChar = driver.find_element_by_id("actualLetter").text

  #starts the lesson
  keyboardpy.press(Keys.ENTER)
  time.sleep(1)
  #types the first char again for update of #remainingText
  keyboardpy.press(currentChar)

  #gets remaining text + currentchar
  remainingText = driver.find_element_by_id("remainingText").text
  currentChar = driver.find_element_by_id("actualLetter").text

  #types the 2nd char
  time.sleep(2)
  keyboardpy.press(currentChar)

  #types every char in the remaining Text
  for char in remainingText:
      keyboardpy.press(char)
      time.sleep(0.15)


      
print(".")
print(".")
print(".")
print("TypeWriterBot by Patrick Cerny, Github: https://github.com/patrickcerny")
print(".")
print(".")
print(".")

print("What Browser do you use? (Firefox: F | Chrome: C | Edge: E")
answerBrowser = input().strip().lower()
if answerBrowser != "e" and answerBrowser != "f" and answerBrowser != "c":
  sys.exit()


print("Do you want to login and do your next Exercise or just do a Excercise without login? (Login: L | Excerice: E)")
answer = input().strip().lower()




if answer == "l":
    driver = Login()
    
    DoExcercise(driver)
elif answer == "e":
    print("Please provide the URL of the excercise:")
    url = input()

    if answerBrowser == "f":
      driver = webdriver.Firefox()
    elif answerBrowser == "c":
      driver = webdriver.Chrome()
    elif answerBrowser == "e":
      driver = webdriver.Edge()  
    
    driver.get(url)
    DoExcercise(driver)



