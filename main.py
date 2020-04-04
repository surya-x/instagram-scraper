import time
from selenium.common.exceptions import NoSuchElementException
from app.utils import *
from app.excel_utils import *
import openpyxl
import os, sys
import shutil

try:
    workbook = openpyxl.load_workbook(r"assets\parameters.xlsx")
    Sheet = workbook.worksheets[0]
    path = Sheet["A1"].value
except:
    print("Parameter.xlsx not found under assets")

if os.path.isdir(path)==False:
    print("Enter the path of directory | Not the path of file : Under parameters.xlsx")
    sys.exit()

driver = connecting_with_chrome()

try:
    login_insta(driver)
except NoSuchElementException:
    print("The Username or Password is incorrect, Try opening it after correcting \nMake sure you have active internet")

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

shutil.move(path + "\insta_search.xlsx", path + "\insta_search_found.xlsx")
driver.quit()
# TODO: change name of insta_search.xlsx

