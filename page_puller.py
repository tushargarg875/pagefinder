import re
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import sqlite3

connect = sqlite3.connect("page_puller.sqlite")
cur = connect.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS Pages(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, html TEXT, search TEXT UNIQUE, clean_status INTEGER)""")
while True:
    search_input = input("Enter what you want to search: ")
    if len(search_input)>1:
        break
    else:
        print("You cannot leave search input empty")
#checking whether there are any special characters
search = re.search("([0-9a-zA-Z]+)",search_input).group(0)
if (search != search_input):
    print("You can not have special characters in your search.")
print("Searching for",search)
cur.execute("""
SELECT * FROM Pages
WHERE search = ?""",(search,))
row = cur.fetchone()
if row is not None:
    print("Data already exists")
    quit()

serverurl="https://web.archive.org/web/*/"
url =serverurl+search
print("Retrieving data")

#Opening chrome in headless mode
WINDOW_SIZE = "1920,1080"
chrome_options = Options()  
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
CHROME_DRIVER_PATH = os.getcwd() + "\chromedriver"

driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH,chrome_options=chrome_options)
driver.get(url)
#Waiting for Js and React to render the webpage
delay = 3 # seconds
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#react-wayback-search .search-result-container li')))
    print ("Page is ready!")
except TimeoutException:
    print ("Loading took too much time!")
element = driver.find_element_by_css_selector("#react-wayback-search")
html = driver.execute_script("return arguments[0].outerHTML;", element)
cur.execute("""
INSERT OR IGNORE INTO Pages(html,search, clean_status)
VALUES(?,?,?)""",(html,search,0))
connect.commit()
cur.close()
print("\n\n===================Retrived Page Successfully===================")
