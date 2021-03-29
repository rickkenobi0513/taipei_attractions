import requests
import json
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

