import re
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import sqlite3
from bs4 import BeautifulSoup
from time import sleep
def csv(res):
    CHROME_DRIVER_PATH = os.getcwd() + "\chromedriver"
    fhandle = open("data.csv",'w')
    fhandle.write("website,captures_per_year")
    conn2 = sqlite3.connect("data.sqlite")
    cur2 = conn2.cursor()
    cur2.execute("""
    SELECT website,webpage_per_year
    FROM Data
    WHERE search = ?
    ORDER BY webpage_per_year desc 
    LIMIT 10""",(res,))
    for i in range(10):
        row = cur2.fetchone()
        try:
            website = row[0]
            per_year = row[1]
        except:
            print("No data associated with that keyword!")
            quit()
        fhandle.write("\n"+str(website)+","+str(per_year))

        
    cur2.close()
    fhandle.close()
    print("Opening your website in 5 seconds. Press refresh to load the website!")
    sleep(10)
    driver2 = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
    html_page = "localhost:8000/index.html"
    driver2.get(html_page)
    try:
        os.system("python -m http.server")
    except:
        os.system("python3 -m http.server")

connect = sqlite3.connect("page_puller.sqlite")
cur = connect.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS Pages(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, html TEXT, search TEXT UNIQUE, clean_status INTEGER)""")
while True:
    search_input = input("Enter what you want to search: ")
    if len(search_input)>0:
        break
    else:
        print("You cannot leave search input empty")
#checking whether there are any special characters
try:
    search = re.search("([0-9a-zA-Z][0-9a-zA-Z ]*)",search_input).group(0)
except:
    print ("Enter valid search keywords!")
    quit()
if (search != search_input):
    print("You can not have special characters in your search.")
search = search.strip()
print("Searching for",search)
cur.execute("""
SELECT * FROM Pages
WHERE search = ?""",(search,))
row = cur.fetchone()
find =0 
if row is not None:
    print("Data already exists")
    find=1
if (find!=1):
    serverurl="https://web.archive.org/web/*/"
    addurl = search.replace(' ','%20')
    url =serverurl+addurl
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
    delay = 10 # seconds
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


conn1 = sqlite3.connect("page_puller.sqlite")
conn2 = sqlite3.connect("data.sqlite")

cur1 = conn1.cursor()
cur2 = conn2.cursor()

cur1.execute("""
SELECT * FROM Pages WHERE clean_status = 0
""")
cur2.execute("""
CREATE TABLE IF NOT EXISTS Data(website TEXT PRIMARY KEY, Captures INTEGER, Start INTEGER, End INTEGER, webpages INTEGER,search TEXT,webpage_per_year INTEGER)
""")

many = 1
for i in range(many):
    row = cur1.fetchone()
    try:
        search = row[2]
    except:
        print ("Everything is cleaned!")
        csv(search)
        quit()
    website_id = row[0]
    soup = BeautifulSoup(row[1],features="lxml")
    container = soup.body.div.contents[1]
    result_list = container.contents[0]
    item = result_list.contents[0]
    for item in result_list:
        div = item.contents[1].contents[0]
        result_heading = div.contents[0]
        result_details = div.contents[2]
        website_raw =       result_heading.contents[0].attrs["href"] #Going down the tree
        distinct_webpages = result_details.contents[0].contents[0].contents[2].text
        Captures=           result_details.contents[1].contents[0].contents[0].text
        Start =             result_details.contents[1].contents[4].contents[0].text
        End =               result_details.contents[1].contents[8].contents[0].text
        website = re.findall(".*(http.*)",website_raw)[0]
        capture_float=""
        prev = 0
        while (Captures[prev:].find(',')!=-1):
            pos = Captures[prev:].find(',')+prev
            capture_float += Captures[prev:pos]
            prev = pos+1
        capture_float+=Captures[prev:]
        webpage_per_year = float(capture_float)/(int(End)-int(Start)+1)
        cur2.execute("""
        INSERT OR IGNORE INTO
        Data(website, Captures, Start, End, webpages,search,webpage_per_year)
        VALUES(?,?,?,?,?,?,?)
        """,(website,Captures,Start,End,distinct_webpages,search,webpage_per_year))
        cur1.execute("""
        UPDATE Pages
        SET clean_status = 1
        WHERE id = ?""",(website_id,) )

conn2.commit()
conn1.commit()
cur1.close()
cur2.close()

csv(search)