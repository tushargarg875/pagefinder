import re
import bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os

search_input = input("Enter what you want to search: ")
if len(search_input)<1:
    search_input = "cricket"            #default keyword search
#checking whether there are any special characters
search = re.search("([0-9a-zA-Z ]+)",search_input).group(0)
if (search != search_input):
    print("You can not have special characters in your search.")
print("Searching for",search)

serverurl="https://web.archive.org/web/*/"
url =serverurl+search
print("Retrieving data")

WINDOW_SIZE = "1920,1080"
chrome_options = Options()  
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
CHROME_DRIVER_PATH = os.getcwd() + "\chromedriver"

driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH,chrome_options=chrome_options)
driver.get(url)
elements = driver.find_elements(By.TAG_NAME, 'div')
for e in elements:
    try:
        print (e.text)
    except: 
        pass
  