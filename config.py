import logging

# File path of contacts.xlsx
credentials_filePath   = r"assets/credentials.xlsx"

# File path of parameters.xlsx
parameters_filePath = r"assets/parameters.xlsx"

insta_search_fileName = r"/insta_search.xlsx"
insta_search_found_fileName = r"/insta_search_found.xlsx"

log_filePath = r"logs/"
logname = log_filePath + 'insta-scraping-logs.log'

logging.basicConfig(level=logging.INFO,
                   # format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(os.getpid()),
                   format='%(asctime)s,%(msecs)d %(levelname)-5s [%(filename)s:%(lineno)d] %(message)s',
                   datefmt='%Y-%m-%d %H:%M:%S',
                   filemode='a+',
                   filename=logname)

logging = logging.getLogger()
