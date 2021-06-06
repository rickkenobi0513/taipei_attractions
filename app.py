from flask import Flask, json
from flask import request
from flask import redirect
from flask import session
from flask import render_template
from flask import jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["JSON_SOIRT_KEYS"] = False

loladb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root!QAZ2wsx"
)

mycursor = loladb.cursor()

def db_connection_check():
    if loladb.is_connected() == False:
        loladb.connect()

@app.route("/")
def index():
    return render_template("homepage.html")

# APIs
@app.route("/api/attractions")
def api_attractions():
    try:
        db_connection_check()
        mycursor = loladb.cursor()
        page = int(request.args.get("page"))
        keyword = request.args.get("keyword", None)
        data = []

        if keyword != None:
            keyword_string = f"WHERE name LIKE '%{keyword}%'"
            page_string = f"WHERE name LIKE '%{keyword}%'"
        else:
            keyword_string = ""
            page_string = ""

        # Fetch attraction data
        query_data_page_info = f"SELECT COUNT(*) FROM website.attraction {page_string};"
        mycursor.execute(query_data_page_info)
        result_page_info = mycursor.fetchall()
        total_page = result_page_info[0][0]//12

        if page >= total_page:
            nextPage = None
        else:
            nextPage = page+1

        query_get_attraction = f'''
                                SELECT id, name, category, description, address, transport, mrt, latitude, longitude
                                FROM website.attraction
                                {keyword_string} LIMIT {(page+1)*12-12},12;
                                '''
        mycursor.execute(query_get_attraction)
        result_attraction = mycursor.fetchall()

        for attraction in result_attraction:
            id = attraction[0]
            # Fetch image data
            img_list = []
            query_get_image = f"SELECT image FROM website.image WHERE attraction_id = {id}"
            mycursor.execute(query_get_image)
            result_image = mycursor.fetchall()

            # Parse image data
            for img in result_image:
                img_list.append(img[0])

            # Make response data
            data.append(
                {
                    "id": attraction[0],
                    "name": attraction[1],
                    "category": attraction[2],
                    "description": attraction[3],
                    "address": attraction[4],
                    "transport": attraction[5],
                    "mrt": attraction[6],
                    "latitude": attraction[7],
                    "longitude": attraction[8],
                    "images": img_list
                }
            )

        return jsonify({"nextPage": nextPage, "data": data})
    except Exception as e:
        return jsonify({"error": True, "message": str(e)})

@app.route("/api/attraction/<attractionId>")
def api_attraction(attractionId):
    try:
        attractionId = str(attractionId)
        db_connection_check()
        mycursor = loladb.cursor()

        # Fetch attracion data
        query_get_attraction = ''' 
        SELECT id, name, category, description, address, transport, mrt, latitude, longitude
        FROM website.attraction
        WHERE id = (%s);
        '''
        mycursor.execute(query_get_attraction, (attractionId,))
        result_attraction = mycursor.fetchall()

        # Fetch image data
        img_list = []
        query_get_image = f"SELECT image FROM website.image WHERE attraction_id = (%s)"
        mycursor.execute(query_get_image, (attractionId,))
        result_image = mycursor.fetchall()

        # Parse image data
        for img in result_image:
            img_list.append(img[0])

        if result_attraction != []:
            # Make response data
            data = {
                "id": result_attraction[0][0],
                "name": result_attraction[0][1],
                "category": result_attraction[0][2],
                "description": result_attraction[0][3],
                "address": result_attraction[0][4],
                "transport": result_attraction[0][5],
                "mrt": result_attraction[0][6],
                "latitude": result_attraction[0][7],
                "longitude": result_attraction[0][8],
                "images": img_list
            }

            return jsonify({"data": data})
        else:
            return jsonify({"error": True, "message": "attactionId doesn't exist!"})
    except Exception as e:
        return jsonify({"error": True, "message": str(e)})

app.run(host="0.0.0.0", port=3000)