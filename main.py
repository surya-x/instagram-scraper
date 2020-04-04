import time
from selenium.common.exceptions import NoSuchElementException
from app.utils import *
from app.excel_utils import *
from config import parameters_filePath, insta_search_fileName, insta_search_found_fileName, logging, credentials_filePath
import openpyxl
import os, sys
import shutil

try:
    print("Process Starting..")
    logging.info("Process Starting..")
    try:
        workbook = openpyxl.load_workbook(parameters_filePath)
        Sheet = workbook.worksheets[0]
        path = Sheet["A1"].value
    except:
        logging.error("Parameter.xlsx not found.")
        print("Error Occurred! | Parameter.xlsx not found ")
        sys.exit()

    if os.path.isdir(path)==False:
        print("Enter the path of directory | Not the path of file : Under parameters.xlsx")
        sys.exit()

    driver = connecting_with_chrome()

    try:
        login_insta(driver, credentials_filePath)
    except NoSuchElementException as e:
        print("The Username or Password is incorrect, Try opening it after correcting \nMake sure you have active internet")
        logging.error(e)
    except Exception as e:
        logging.error(e)

    # login_insta(driver)
    time.sleep(10)

    ID = read_excel(path,2,2)[0]
    scrap_master(driver, ID)

    follower_list = get_followers(driver)
    write_excel(path, 3, 1, follower_list)

    write_excel(path, 2, 2, ["OK"])

    nrows = get_num_of_rows(path)
    all_children = read_excel(path, 3, nrows)

    rank = 2

    for children in all_children:
        rank = rank + 1

        scrap_master(driver, children)

        follower_list = get_followers(driver)

        nrows = get_num_of_rows(path)
        write_excel(path, nrows+1 , 1, follower_list)

        if len(follower_list) > 0:
            write_excel(path, rank, 2, ["OK"])

    shutil.move(path + insta_search_filePath, path + insta_search_found_filePath)
    driver.quit()
    # TODO: change name of insta_search.xlsx
except Exception as e:
    print("Error Occurred!.")
    logging.error(e)
