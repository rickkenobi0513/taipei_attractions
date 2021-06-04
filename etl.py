import requests
import json
import mysql.connector

sysdb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root!QAZ2wsx"
)

mycursor = sysdb.cursor()

data = requests.get(url="https://padax.github.io/taipei-day-trip-resources/taipei-attractions.json")
rwdata = data.content.decode("utf-8")
d_data = json.loads(rwdata)
result = d_data["result"]
results = result["results"]

for r in results:
    id = r["_id"]
    name = r["stitle"]
    category = r["CAT2"]
    description = r["xbody"]
    address = r["address"]
    transport = r["info"]
    mrt = r["MRT"]
    longitude = r["longitude"]
    latitude = r["latitude"]
    file = r["file"]
    sp_file = ["http://" + f for f in file.split(sep="http://")[1:]]

    # Load data into database
    def data_check(table):
        if table == "attraction":
            col = "id";
        elif table == "image":
            col = "attraction_id"
        query_check = f"SELECT * FROM website.{table} WHERE {col}=(%s)"
        mycursor.execute(query_check, (id,))
        check = mycursor.fetchall()
        return check
    # attraction table
    if data_check("attraction") == []:
        query_attraction = '''
                            INSERT INTO website.attraction(id, name, category, description, address, transport, mrt, latitude, longitude)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                           '''
        mycursor.execute(query_attraction, (id, name, category, description, address, transport, mrt, latitude, longitude ))
        sysdb.commit()

    if data_check("image") == []:
        for image in sp_file:
            query_image = "INSERT INTO website.image(attraction_id, image) VALUES (%s, %s)"
            mycursor.execute(query_image, (id, image))
        sysdb.commit()
    
 

            