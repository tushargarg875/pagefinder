import sqlite3
fhandle = open("data.csv",'w')
fhandle.write("website,captures_per_year")
conn2 = sqlite3.connect("data.sqlite")
cur2 = conn2.cursor()
cur2.execute("""
SELECT website,webpage_per_year
FROM Data
ORDER BY webpage_per_year desc 
LIMIT 10""")
for row in cur2:
    website = row[0]
    per_year = row[1]
    fhandle.write("\n"+str(website)+","+str(per_year))
cur2.close()