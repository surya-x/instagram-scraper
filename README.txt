
# Instagram scraper

This scraper is developed to scrap the followers of anyone using their Username.
It will run by starting "main.py"

It will work in the following steps :-
1. It will log into instagram using username and password stored in credentials.xlsx
2. It will use the parameters.xlsx to get the location of file "insta_search.xlsx"  
3. It will first read the ID(master ID) written in file "insta_search.xlsx".
4. Then will scrap all the followers of the ID written in "insta_search.xlsx" and paste them below the already written ID(master ID).
5. Then For all the ID's below master ID (which are pasted by the #instagram-scraper), the scraper will scrap the followers of those too.
6. And will paste them under initially scrapped ID's.
7. After completing by its own then only it will change the name of file from "insta_search.xlsx" to "insta_search_found.xlsx".

Note :- 
    > Make sure you are writing the path(location) of directory(folder) in which "insta_search.xlsx" is there, in "parameter.xlsx". Not the path of the file itself.
    > Example :- 
      It should be like -- C:\Python\Projects\Insta_followers\assets
      Not like          -- C:\Python\Projects\Insta_followers\assets\insta_search.xlsx
    > The program (bot) will automatically stop if it reach the limit of rows in excel. That is around 1M followers.
    > You can anytime stop the bot in between, you will still have the ID's scrapped inside "insta_search.xlsx".
    
    
 For Technical Information
 The library's used :- 
    selenium
    openpyxl
    time
    itertool
    explicit
    shutil
    os
    sys
