from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from explicit import waiter
import logging
import itertools

from app.excel_utils import *

def connecting_with_chrome():
    try:
        logging.info("connecting_with_chrome called!")
        options = webdriver.ChromeOptions()
        # options.add_argument("-headless")
        driver = webdriver.Chrome(options=options)
        return driver
    except Exception as e:
        print("Error : loading Chrome")
        logging.error(e)

def login_insta(driver, credentials_filePath):
    try:
        logging.info("login_insta called! for :" + str(credentials_filePath))
        workbook = openpyxl.load_workbook(credentials_filePath)
        Sheet_login = workbook.worksheets[0]
        logging.info(Sheet_login["B1"].value + " | " + Sheet_login["B2"].value)
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
    except NoSuchElementException as e:
        # print("The Username or Password is incorrect, Try opening it after correcting \nMake sure you have active internet")
        logging.error(e)
        return False
    except Exception as e:
        print("Error while Fetching username/password from credentials.xlsx")
        logging.error(e)
        return False
    return True


def scrap_master(driver, masterid):
    logging.info("scrap_master called!")
    driver.get("https://www.instagram.com/" + masterid)
    try:
        followers = driver.find_element(By.PARTIAL_LINK_TEXT, "followers")
        followers.click()
    # except NoSuchElementException:
    #     followers = driver.find_element(By.PARTIAL_LINK_TEXT, "follower")
    #     followers.click()
    except NoSuchElementException as nse:
        try:
            followers = driver.find_element(By.PARTIAL_LINK_TEXT, "follower")
            followers.click()
        except NoSuchElementException as e:
            print("The ID - " + masterid + " is private")
            print("Skipping the ID...")
            logging.error(e)
        logging.error(nse)
        return False
    return True

    # num_of_followers = driver.find_element_by_css_selector("ul li:nth-child(2) span").text

def get_followers(driver):
    # Followers popup window must be open before using the method
    # limit = int(limit)
    logging.info("get_followers called!")
    follower_list = []
    follower_css = "ul div li:nth-child({}) a.notranslate"  # Taking advange of CSS's nth-child functionality

    try:
        for group in itertools.count(start=1, step=12):
            for follower_index in range(group, group + 12):
                follower_list.append( waiter.find_element(driver, follower_css.format(follower_index)).text)
                # print( waiter.find_element(driver, follower_css.format(follower_index)).text)

            last_follower = waiter.find_element(driver, follower_css.format(follower_index))
            driver.execute_script("arguments[0].scrollIntoView();", last_follower)
    except TimeoutException as te:
        print("done")
        logging.info("Process Completed with TimeoutException!")
        logging.info(te)
    finally:
        logging.info("Process Completed!")
        return follower_list

