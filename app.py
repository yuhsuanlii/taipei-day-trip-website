from flask import *
from mysql.connector import pooling

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"]=False
app.config['SECRET_KEY'] = b'\x8f\xef\xa5\xba#8.9\xa5A]\xdd\xc4\x1b\x8d\x0c'

def get_connection():
    connection = pooling.MySQLConnectionPool(
        pool_name = "python_pool",
        pool_size = 20,
        pool_reset_session = True,
        host = 'localhost',
        user = 'root',
        password = 'root',
        database = 'daytrip'
        )
    conn = connection.get_connection()
    return conn

# API
@app.route("/api/attractions", methods=["GET"])
def attractions():
    keyword = request.args.get("keyword", "")
    page = request.args.get("page", 0)
    page = int(page)
    if page is None:
        page = 0
    page_size = 12
    
    try:
        conn = get_connection()
        cur = conn.cursor()
        if keyword=="":
            sql = "SELECT * FROM attraction LIMIT %s, %s"
            cur.execute(sql,(page*page_size,12))
        else:
            sql = "SELECT * FROM attraction WHERE name REGEXP %s OR category= %s LIMIT %s, %s"
            cur.execute(sql,(str(keyword),str(keyword),page*page_size,12))
        record = cur.fetchall()
    
        if len(record)>0:
            result = []
            for i in range(len(record)):
                data_dic = {}
                data_dic["id"] = record[i][0]
                data_dic["name"] = record[i][1]
                data_dic["category"] = record[i][2]
                data_dic["description"] = record[i][3]
                data_dic["address"] = record[i][4]
                data_dic["transport"] = record[i][5]
                data_dic["mrt"] = record[i][6]
                data_dic["latitude"] = record[i][7]
                data_dic["longitude"] = record[i][8]
                data_dic["images"] = record[i][9].split(", ")

                result.append(data_dic)

                if len(record) == page_size:
                    page_data = (page+1)
                else:
                    page_data = None
                data = {"nextPage": page_data, "data": result}
                response = app.response_class(response=json.dumps(data),
                                         status=200, content_type='application/json')
            return response
        else:
            data = {"nextPage": None, "data": []}
            response = app.response_class(response=json.dumps(data),
                                         status=200, content_type='application/json')
            return response
    except Exception as e:
        print(e)
        fail = {"error": True,"message": "伺服器內部錯誤"}
        response = app.response_class(response=json.dumps(fail),
                                    status=500, content_type='application/json')
        return response
    finally:
        cur.close()
        conn.close()


@app.route("/api/attraction/<attractionId>", methods=['GET'])
def attractionId(attractionId):
    conn = get_connection()
    cur = conn.cursor()
    sql = "SELECT * FROM attraction WHERE id = %s"
    id = (str(attractionId),)
    cur.execute(sql,id)
    record = cur.fetchall()
    try:
        if len(record) > 0:
            for i in range(len(record)):
                data_dic = {}
                data_dic["id"] = record[i][0]
                data_dic["name"] = record[i][1]
                data_dic["category"] = record[i][2]
                data_dic["description"] = record[i][3]
                data_dic["address"] = record[i][4]
                data_dic["transport"] = record[i][5]
                data_dic["mrt"] = record[i][6]
                data_dic["latitude"] = record[i][7]
                data_dic["longitude"] = record[i][8]
                data_dic["images"] = record[i][9].split(", ")

            return make_response(jsonify(data = data_dic),200,
                                    {'ContentType':'application/json'})
        else:
            nodata = {"error":True,"message":"沒有此景點編號"}
            response = app.response_class(response=json.dumps(nodata),
                                        status=400,content_type='application/json')
            return response
    
    except Exception as e:
        print(e)
        fail = {"error": True,"message": "伺服器內部錯誤"}
        response = app.response_class(response=json.dumps(fail),
                                    status=500, content_type='application/json')
        return response
    finally:
        cur.close()
        conn.close()

@app.route("/api/categories", methods=['GET'])
def categories():
    conn = get_connection()
    cur = conn.cursor()
    sql = "SELECT category FROM attraction"
    cur.execute(sql)
    data = cur.fetchall()
    try:
        json_data = []
        for i in list(set(data)):
            res = "".join(i)
            json_data.append(res)
        return make_response(jsonify(data = json_data),200,
                            {'ContentType':'application/json'})    
    except Exception as e:
        print(e)
        fail = {"error": True,"message": "伺服器內部錯誤"}
        response = app.response_class(response=json.dumps(fail),
                                    status=500, content_type='application/json')
        return response
    finally:
        cur.close()
        conn.close()

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)