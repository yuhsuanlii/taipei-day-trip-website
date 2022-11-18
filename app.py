from flask import *
import pymysql

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"]=False

app.config['SECRET_KEY'] = b'\x8f\xef\xa5\xba#8.9\xa5A]\xdd\xc4\x1b\x8d\x0c'
conn = pymysql.connect(host='localhost',user='root',password='rootroot',db='daytrip',charset='utf8')
cur = conn.cursor()

# API
@app.route("/api/attractions", methods=["GET"])
def attractions():
    keyword = request.args.get("keyword", "")
    page = request.args.get("page", 0)
    page = int(page)
    if page is None:
        page = 0
    page_size = 12
    
    if keyword=="":
        sql = "SELECT * FROM attraction LIMIT %s, 12"
        params = (page*page_size)
    else:
        sql = "SELECT * FROM attraction WHERE name REGEXP %s OR category= %s LIMIT %s, 12"
        params = (str(keyword),str(keyword),page*page_size)
    cur.execute(sql,params)
    record = cur.fetchall()
    
    try:
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
                
                imgsql = "SELECT images FROM attraction where id = %s"
                params = record[i][0],
                cur.execute(imgsql,params)
                imgdata = cur.fetchall()
                for imgurl in imgdata:
                    img_arr = "".join(imgurl).split(", ")
                    data_dic["images"] = img_arr

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

@app.route("/api/attraction/<attractionId>", methods=['GET'])
def attractionId(attractionId):
    sql = "SELECT * FROM attraction WHERE id = %s"
    params = attractionId
    cur.execute(sql,params)
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

                imgsql = "SELECT images FROM attraction where id = %s"
                params = record[i][0],
                cur.execute(imgsql,params)
                imgdata = cur.fetchall()
                for imgurl in imgdata:
                    img_arr = "".join(imgurl).split(", ")
                    data_dic["images"] = img_arr

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

@app.route("/api/categories", methods=['GET'])
def categories():
    sql = "SELECT category FROM attraction"
    cur.execute(sql)
    data = cur.fetchall()
    try:
        json_data = []
        for i in list(set(data)):
            res = "".join(i)
            json_data.append(res)
        print(json_data)
        return make_response(jsonify(data = json_data),200,
                            {'ContentType':'application/json'})    
    except Exception as e:
        print(e)
        fail = {"error": True,"message": "伺服器內部錯誤"}
        response = app.response_class(response=json.dumps(fail),
                                    status=500, content_type='application/json')
        return response


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