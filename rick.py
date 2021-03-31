import requests
import json
import mysql.connector

sysdb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root"
)

mycursor = sysdb.cursor()

data = requests.get(url="https://data.taipei/api/v1/dataset/36847f3f-deff-4183-a5bb-800737591de5?scope=resourceAquire")
rwdata = data.content.decode("utf-8")
d_data = json.loads(rwdata)
result = d_data["result"]
results = result["results"]
for r in results:
    stitle = r["stitle"]
    longitude = r["longitude"]
    latitude = r["latitude"]
    file = r["file"]
    sp_file = file.split(sep="http://")
    co_file = "http://" + sp_file[1]

    with open("resort_info.txt","a", encoding="utf-8") as resort:
        resort.write(", ".join([stitle,longitude,latitude,co_file]))
        resort.write("\n") 
    query = """
       SELECT * FROM attractions.attraction_info where stitle = (%s) ;
        """
    mycursor.execute(query,(stitle,))
    fetch = mycursor.fetchall()
    
    if fetch == [] :
        query1 = """
            INSERT INTO attractions.attraction_info(stitle,longitude,latitude,file) values (%s,%s,%s,%s); 
            """      
        mycursor.execute(query1,(stitle,longitude,latitude,co_file))
        sysdb.commit()


            