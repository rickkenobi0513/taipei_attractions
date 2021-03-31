import mysql.connector
import pandas as pd

sysdb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root"
)

mycursor = sysdb.cursor()
query = """
        SELECT * FROM attractions.attraction_info 
        """
mycursor.execute(query)
fetch = mycursor.fetchall()
stitle = []
longitude = []
latitude = []
file = []
for data in fetch:
    stitle.append(data[1])
    longitude.append(data[2])
    latitude.append(data[3])
    file.append(data[4])
attdict = {"s":stitle,"lo":longitude,"la":latitude,"f":file}
df = pd.DataFrame(data=attdict)
df.to_excel("Taipei_attraction.xlsx")  
