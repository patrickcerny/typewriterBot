import sys
import time

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By

#chrome driver download
from webdriver_manager.chrome import ChromeDriverManager



def Exit(exit: bool, errorMessage: str):
    """
    Prints an error (and possibly exits the application)

    Args:
        exit (bool): Bool which indicates, wether the application should close or not
        errorMessage (str): Errormessage that the user wants to display
    """
    print("Error! Something went wrong!")
    print("Error Message: " + errorMessage)
    if exit:
        print("Press Enter to exit.")
        input()
        sys.exit(0)


def GetChromeDriver():
    """
    Tries to initialize a ChromeDriver instance with the newest ChromeDriver

    Returns:
        webdriver
    """
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def LoginUser():
    """
    Asks the User for his/hers credentials and logs him into his account.
    """
    print(
        "Hello User!\n"
        "This is a warning! This application has to use your typetrainer username and password! "
        "The credentials will not be saved in any way. They serve for login purposes only.\n"
        "Do you want to continue? (Y/n)"
    )
    answer = input().strip().lower()

    if answer == "n":
        Exit(True, "You didn't want to login :(")

    print("Please Enter your Username:")
    username = input().strip()
    
    print("Please Enter your Password:")
    password = input().strip()
   
    driver = GetChromeDriver()

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
    """
    Tries to find the button for the 

    Args:
        driver (any): Currently active Webdriver

    Returns:
        driver (any): Currently active Webdriver
    """
    time.sleep(1)
    try:
        linkToLesson = driver.find_element(By.CLASS_NAME, "cockpitStartButton")
        linkToLesson.click()
    except Exception as e:
        Exit(True, str(e))


