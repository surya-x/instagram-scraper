from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from explicit import waiter
import itertools

from app.excel_utils import *

def connecting_with_chrome():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("-headless")
        driver = webdriver.Chrome(options=options)
        return driver
    except:
        print("Error : loading Chrome")

def login_insta(driver):
    try:
        workbook = openpyxl.load_workbook(r"assets\credentials.xlsx")
        Sheet_login = workbook.worksheets[0]

        username = Sheet_login["B1"].value
        password = Sheet_login["B2"].value
    # scrap this from excel (credentials.xlsx)

        driver.get("https://www.instagram.com/accounts/login/")
        user_input = driver.find_element(By.NAME,"username")
        pass_input = driver.find_element(By.NAME,"password")

        user_input.send_keys(username)
        pass_input.send_keys(password, Keys.RETURN)
    # sleep here 1-2 sec
    # wait = driver.find_element(By.XPATH,"//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[4]")
    except:
        print("Error : Fetching username/password from credentials.xlsx")


def scrap_master(driver, masterid):
    driver.get("https://www.instagram.com/" + masterid)
    try:
        followers = driver.find_element(By.PARTIAL_LINK_TEXT, "followers")
        followers.click()
    # except NoSuchElementException:
    #     followers = driver.find_element(By.PARTIAL_LINK_TEXT, "follower")
    #     followers.click()
    except NoSuchElementException:
        try:
            followers = driver.find_element(By.PARTIAL_LINK_TEXT, "follower")
            followers.click()
        except NoSuchElementException:
            print("The ID - " + masterid + " is private")
            print("Skipping the ID...")

    # num_of_followers = driver.find_element_by_css_selector("ul li:nth-child(2) span").text

def get_followers(driver):
    # Followers popup window must be open before using the method
    # limit = int(limit)
    follower_list = []
    follower_css = "ul div li:nth-child({}) a.notranslate"  # Taking advange of CSS's nth-child functionality

    try:
        for group in itertools.count(start=1, step=12):
            for follower_index in range(group, group + 12):
                follower_list.append( waiter.find_element(driver, follower_css.format(follower_index)).text)
                # print( waiter.find_element(driver, follower_css.format(follower_index)).text)

            last_follower = waiter.find_element(driver, follower_css.format(follower_index))
            driver.execute_script("arguments[0].scrollIntoView();", last_follower)
    except TimeoutException:
        print("done")
    finally:
        return follower_list

