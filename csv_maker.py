import sqlite3
fhandle = open("data.csv",'w')
res = input("Enter the search you want to visualise:")
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