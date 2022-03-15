from argparse import Action
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from getpass import getpass


def writeToFile(text):
    file = open("user_data.txt", "w")
    file.writelines(text)
    file.close()

####################################################
#  Global Variables
####################################################

username = ""
password = ""
browser = ""


####################################################

def checkBrowser():
    try:
        print("Checking preferred browser...")
        file = open("user_browser.txt", "r")
        browser = file.readline()
        file.close()
    except:
        browser = input("Please select your installed browser" + "\n1. Chrome" + "\n2. Firefox" + "\n3. Brave\n")
        file = open("user_browser.txt", "w+")
        file.writelines(browser)
        file.close()
    finally:
        return browser

def initiateBrowser(browser):
    #driver = webdriver
    if browser == "1":
        print("Preferred browser is Chrome.")
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=option)
        return driver
    elif browser == "2":
        print("Preferred browser is Firefox.")
        driver = webdriver.Firefox()
        driver.maximize_window()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") 
        return driver
    elif browser == "3":
        print("Preferred browser is Brave.")
        driver_path = "chromedriver.exe"
        brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
        option = webdriver.ChromeOptions()
        option.binary_location = brave_path
        option.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(executable_path=driver_path, chrome_options=option)
        return driver

def checkTextfile():
    print("Trying to open user data textfile...")
    try:
        file = open("user_data.txt", "r")
        print("File found. Retreiving values...")
        username = file.readline().strip()
        password = file.readline().strip()
    except:
        print("No File Found. Creating...")
        username = input("\nPlease enter the student number used for login:\n")
        open("user_data.txt", "w+")
        password = getpass("Please enter the password associated with the student number:\n")
        writeToFile(username + "\n" + password)
    finally:
        doCovidScreening(username, password)
        

def doCovidScreening(username, password):
    browser = checkBrowser()
    driver = initiateBrowser(browser)
    driver.get("https://workflow7prd.nwu.ac.za/covid-screening/?locale=en_ZA")
    
    try: 
        elem = driver.find_element(By.ID, "username")
        elem.clear()
        elem.send_keys(username)
        elem = driver.find_element(By.ID, "password")
        elem.send_keys(password)
        elem.send_keys(Keys.RETURN)
    except:
        print("Cannot find login fields")

    try: 
        elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "gwt-uid-2")))
        elem = driver.find_element(By.ID, "gwt-uid-2")
        action = ActionChains(driver)
        action.move_to_element(elem).click().perform()
    except:
        print("Cannot find disclaimer checkbox")

    try:
        elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "gwt-uid-45")))
        elem.send_keys(Keys.END)
        time.sleep(1)
        elem = driver.find_element(By.ID, "gwt-uid-45")
        action.move_to_element(elem).click().perform()
        elem = driver.find_element(By.ID, "gwt-uid-55")
        action.move_to_element(elem).click().perform()
        elem = driver.find_element(By.ID, "gwt-uid-51")
        action.move_to_element(elem).click().perform()
        elem = driver.find_element(By.ID, "gwt-uid-57")
        action.move_to_element(elem).click().perform()
        elem = driver.find_element(By.ID, "gwt-uid-59")
        action.move_to_element(elem).click().perform()
        elem = driver.find_element(By.ID, "gwt-uid-63")
        action.move_to_element(elem).click().perform()
        elem = driver.find_element(By.ID, "gwt-uid-53")
        action.move_to_element(elem).click().perform()
        elem = driver.find_element(By.ID, "gwt-uid-61")
        action.move_to_element(elem).click().perform()
        elem = driver.find_element(By.ID, "gwt-uid-49")
        action.move_to_element(elem).click().perform()
        elem = driver.find_element(By.ID, "gwt-uid-47")
        action.move_to_element(elem).click().perform()
        elem = driver.find_element(By.ID, "gwt-uid-43")
        action.move_to_element(elem).click().perform()
        elem = driver.find_element(By.ID, "submit")
        elem.click()
        print("Automated Screening Complete. Waiting for submission...")
        time.sleep(15)
    except:
        print("Not found")
        time.sleep(15)

    driver.close()

checkTextfile()