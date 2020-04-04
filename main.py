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
        print("Error Occurred!")
        sys.exit()

    if os.path.isdir(path)==False:
        print("Enter the path of directory | Not the path of file : Under parameters.xlsx")
        sys.exit()

    driver = connecting_with_chrome()

    if login_insta(driver, credentials_filePath):
        # login_insta(driver)
        time.sleep(10)

        ID = read_excel(path,2,2)[0]

        if scrap_master(driver, ID):
            follower_list = get_followers(driver)
            write_excel(path, 3, 1, follower_list)

            write_excel(path, 2, 2, ["OK"])

            nrows = get_num_of_rows(path)
            all_children = read_excel(path, 3, nrows)

            rank = 2

            for children in all_children:
                rank = rank + 1

                if scrap_master(driver, children):

                    follower_list = get_followers(driver)

                    nrows = get_num_of_rows(path)
                    write_excel(path, nrows+1 , 1, follower_list)

                    if len(follower_list) > 0:
                        write_excel(path, rank, 2, ["OK"])

            shutil.move(path + insta_search_filePath, path + insta_search_found_filePath)
    else:
        print("Something wrong with login!.\n Exiting..")
    driver.quit()
    # TODO: change name of insta_search.xlsx
except Exception as e:
    print("Error Occurred!.")
    logging.error(e)
