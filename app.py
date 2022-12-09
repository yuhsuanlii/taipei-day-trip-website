from flask import *
from mysql.connector import pooling
import re
import jwt
from flask_bcrypt import generate_password_hash, check_password_hash

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
        password = 'rootroot',
        database = 'daytrip'
        )
    conn = connection.get_connection()
    return conn

# Attractions API
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


# User API
@app.route("/api/user", methods=['POST'])
def post_user():
    name=request.json["name"]
    email=request.json["email"]
    password=request.json["password"]
    email_check = re.match("^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$", email)
    password_check = re.match("[a-zA-Z0-9]{4,12}", password) # 4-12英數字

    if name == None or email_check == None or password_check == None:
        response = jsonify({"error": True,"message": "資料格式錯誤"})
        response.status_code = "400"
        return response
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE email = %s",[email])
        result = cur.fetchone()
        # print(result)
        if not result == None:
            response = jsonify({"error": True,"message": "Email已重覆註冊"})
            response.status_code = "400"
            return response
        # if result == None:
        hash_password = generate_password_hash(password).decode('utf-8')
        cur.execute("INSERT INTO user (name, email, password) VALUES (%s, %s, %s)", [name, email, hash_password])
        conn.commit()
        response = jsonify({"ok":True})
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


@app.route("/api/user/auth", methods=['PUT'])
def put_user():
    email=request.json["email"]
    password=request.json["password"]
    email_check = re.match("^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$", email)
    password_check = re.match("[a-zA-Z0-9]{4,12}", password) # 4-12英數字
    if  email_check == None or password_check == None:
        response = jsonify({
            "error": True,
            "message": "無此帳號"
        })
        response.status_code = "400"
        return response
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary = True)
        cur.execute("SELECT id, name, email, password FROM user WHERE email = %s",[email])
        result = cur.fetchone()
        if result == None:
            response = jsonify({
                "error": True,
                "message": "電子信箱或密碼輸入錯誤"
            })
            response.status_code = "400"
            return response
        hash_password_check = check_password_hash(result["password"], password)
        if hash_password_check == False:
            response = jsonify({
                "error": True,
                "message": "電子信箱或密碼輸入錯誤"
            })
            response.status_code = "400"
            return response
        JWT_data = {
            "id": result["id"],
            "name": result["name"],
            "email": result["email"]
        }
        encoded_jwt = jwt.encode(JWT_data, 'secret_key', algorithm="HS256")
        response = make_response(jsonify({"ok": True}))
        print(encoded_jwt)
        response.set_cookie(key = "token", value = encoded_jwt, max_age = 604800) #7天
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


@app.route("/api/user/auth", methods=['GET'])
def get_user():
    JWT_cookies = request.cookies.get("token")
    if JWT_cookies == None:
        response = jsonify({"data": None})
        return response
    decoded_jwt = jwt.decode(JWT_cookies, 'secret_key', algorithms="HS256")
    response = jsonify({"data":decoded_jwt})
    return response


@app.route("/api/user/auth", methods=['DELETE'])
def delete_user():
    response = make_response(jsonify({"ok": True}))
    response.delete_cookie("token")
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