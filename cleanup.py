from bs4 import BeautifulSoup
import sqlite3
import re
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

# many = input("How many to clean?")
# many = int(many)
row = cur1.fetchone()
search = row[2]
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