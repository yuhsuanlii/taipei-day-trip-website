from flask import *
from mysql.connector import pooling
import re
import jwt
from flask_bcrypt import generate_password_hash, check_password_hash
from datetime import *
import requests
import os
from dotenv import load_dotenv

load_dotenv('.env')
partner_key = os.getenv("PARTNER_KEY")
merchant_id = os.getenv("MERCHANT_ID")
mysql_user = os.getenv("MYSQL_USER")
mysql_pwd = os.getenv("MYSQL_PASSWORD")
mysql_db = os.getenv("MYSQL_DATABASE")

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"]=False

def get_connection():
    connection = pooling.MySQLConnectionPool(
        pool_name = "python_pool",
        pool_size = 20,
        pool_reset_session = True,
        host = 'localhost',
        user = mysql_user,
        password = mysql_pwd,
        database = mysql_db
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


# Booking API
@app.route("/api/booking", methods=['POST'])
def post_booking():
    attractionId = request.json["attractionId"]
    date = request.json["date"]
    time = request.json["time"]
    price = request.json["price"]
    today = datetime.now().strftime('%Y-%m-%d')

    # 如果cookie沒有token
    JWT_cookies = request.cookies.get("token")       
    if JWT_cookies == None:
        response = jsonify({"error": True,"message": "請先登入系統"})
        response.status_code = "403"
        return response
    if  date == "":
        response = jsonify({"error": True,"message": "請選擇預約日期"})
        response.status_code = "400"
        return response
    decoded_jwt = jwt.decode(JWT_cookies, 'secret_key', algorithms="HS256")
    userId = decoded_jwt["id"]

    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM booking WHERE userId = %s AND date = %s AND time = %s", [userId, date, time])
        result = cur.fetchone()
        if result != None:
            response = jsonify({ "error": True, "message": "此日期時間已預定" })
            response.status_code = "400"
            return response
        if  date < today:
            response = jsonify({ "error": True, "message": "無法選擇過去日期" })
            response.status_code = "400"
            return response
        cur.execute("INSERT INTO booking (attractionId, date, time, price, userId) VALUES (%s, %s, %s, %s, %s);", [attractionId, date, time, price, userId])
        conn.commit()
        response = jsonify({ "ok": True })
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


@app.route("/api/booking", methods=['GET'])
def get_booking():
    JWT_cookies = request.cookies.get("token")
    if JWT_cookies == None:
        response = jsonify({"error": True,"message": "請先登入系統"})
        response.status_code = "403"
        return response
    decoded_jwt = jwt.decode(JWT_cookies, 'secret_key', algorithms="HS256")
    userId = decoded_jwt["id"]

    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT booking.id, attractionId, name, address, images, date, time, price FROM booking INNER JOIN attraction ON attraction.id = booking.attractionId WHERE userId = %s ORDER BY booking.id DESC LIMIT 1",[userId])
        result=cur.fetchone()
        if result != None:
            alldata = {
                    "attraction":{
                        "id": result["attractionId"],
                        "name": result["name"],
                        "address": result["address"],
                        "image": result['images'].split(", ")[0]
                    },
                    "date": str(result["date"]),
                    "time": result["time"],
                    "price": result["price"]
                }  
            response = jsonify({ "data": alldata })
            print(response)
            return response
        response = jsonify({ "data": None })
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


@app.route("/api/booking", methods=['DELETE'])
def delete_booking():
    JWT_cookies = request.cookies.get("token")
    response = make_response(jsonify({"ok": True}))
    if JWT_cookies == None:
        response = jsonify({"error": True,"message": "請先登入系統"})
        response.status_code = "403"
        return response
    decoded_jwt = jwt.decode(JWT_cookies, 'secret_key', algorithms="HS256")
    userId = decoded_jwt["id"]
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        # 一個一個刪
        # cur.execute("DELETE FROM booking WHERE userId = %s AND attractionId = %s AND date = %s AND time = %s", [userId, attractionId, date, time])
        # 只要是這個userId全部刪除
        cur.execute("DELETE FROM booking WHERE userId = %s", [userId])
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


# Orders API
@app.route("/api/orders", methods=['POST'])
def post_orders():

    JWT_cookies = request.cookies.get("token")       
    if JWT_cookies == None:
        response = jsonify({"error": True,"message": "請先登入系統"})
        response.status_code = "403"
        return response
    
    decoded_jwt = jwt.decode(JWT_cookies, 'secret_key', algorithms="HS256")
    userId = decoded_jwt["id"]

    data = request.get_json()
    print(data)
    prime = data["prime"]
    order = data["order"]["trip"]
    contactName = data["contact"]["name"]
    contactEmail = data["contact"]["email"]
    contactPhone = data["contact"]["phone"]
    attractionId = data["order"]["trip"]["attraction"]["id"]
    date = data["order"]["trip"]["date"]
    time = data["order"]["trip"]["time"]
    price = data["order"]["trip"]["price"]

    # 20221223+時分+會員id+景點id
    now = datetime.now()
    order_number = now.strftime("%Y%m%d%H%M") + str(userId) + str(attractionId)

    if contactName=="" or contactEmail=="" or contactPhone=="":
        response = jsonify({"error": True,"message": "訂單建立失敗，請確認填寫資料"})
        response.status_code = "400"
        return response

    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)     
        cur.execute("INSERT INTO orders (number, userId, attractionId, date, time, price, contactName, contactEmail, phone, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",[order_number, userId, attractionId, date, time, price, contactName, contactEmail, contactPhone, "未付款"])
        conn.commit()
        # 刪除購物車資料
        cur.execute("DELETE FROM booking WHERE userId = %s", [userId])
        conn.commit()

        # TapPay
        url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": partner_key
        }
        data = {
            "prime": prime,
            "partner_key": partner_key,
            "merchant_id": merchant_id,
            "details": f"Taipei Day Trip - Order Number: {order_number}",
            "amount": price,
            "cardholder": {
                "phone_number": contactPhone,
                "name": contactName,
                "email": contactEmail
            },
            "remember": True
        }

        tappay = requests.post(url, headers = headers, json = data).json()
        print("tappay status: " + str(tappay["status"]))

        if tappay["status"] != 0:
            response = jsonify({
                "data": {
                    "number": order_number,
                    "payment": {
                        "status": tappay["status"],
                        "message": "付款失敗"
                        }
                }
            })
            return response
            
        cur.execute("UPDATE orders SET status = %s WHERE number = %s", ["已付款", order_number])
        conn.commit()
        response = jsonify({
            "data": {
                "number": order_number,
                "payment": {
                    "status": tappay["status"],
                    "message": "付款成功"
                    }
            }
        })
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


@app.route("/api/orders/<orderNum>", methods=['GET'])
def get_orders(orderNum):
    
    JWT_cookies = request.cookies.get("token")       
    if JWT_cookies == None:
        response = jsonify({"error": True,"message": "請先登入系統"})
        response.status_code = "403"
        return response
    decoded_jwt = jwt.decode(JWT_cookies, 'secret_key', algorithms="HS256")
    userId = decoded_jwt["id"]
    
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT orders.*, attraction.id, attraction.name, attraction.address, attraction.images FROM orders INNER JOIN attraction ON attraction.id = orders.attractionId WHERE orders.userId = %s AND orders.number = %s",[userId, orderNum])
        result = cur.fetchone()
        # print(result)
        if result != None:
            orderdata = {
                    "number": result["number"],
                    "price": result["price"],
                    "trip":{
                        "attraction":{
                            "id": result["attractionId"],
                            "name": result["name"],
                            "address": result["address"],
                            "image": result['images'].split(", ")[0]
                        },
                        "date": str(result["date"]),
                        "time": result["time"],
                    },
                    "contact":{
                        "name": result["contactName"],
                        "email": result["contactEmail"],
                        "phone": result["phone"]
                    },
                    "status":result["status"]
                }  
            response = jsonify({ "data": orderdata })
            # print(orderdata)
            return response
        response = jsonify({ "data": None })
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


@app.route("/api/order", methods=['GET'])
def get_orderlist():
    
    JWT_cookies = request.cookies.get("token")       
    if JWT_cookies == None:
        response = jsonify({"error": True,"message": "請先登入系統"})
        response.status_code = "403"
        return response
    decoded_jwt = jwt.decode(JWT_cookies, 'secret_key', algorithms="HS256")
    userId = decoded_jwt["id"]
    
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT orders.*, attraction.id, attraction.name, attraction.address, attraction.images FROM orders INNER JOIN attraction ON attraction.id = orders.attractionId WHERE orders.userId = %s ORDER BY orders.id DESC",[userId])
        result = cur.fetchall()
        # print(result)
        if result != []:
            data = []
            for i in result:
                data_group = {
                    "number": i["number"],
                    "price": i["price"],
                    "trip":{
                        "attraction":{
                            "id": i["attractionId"],
                            "name": i["name"],
                            "address": i["address"],
                            "image": i['images'].split(", ")[0]
                        },
                        "date": str(i["date"]),
                        "time": i["time"],
                    },
                    "contact":{
                        "name": i["contactName"],
                        "email": i["contactEmail"],
                        "phone": i["phone"]
                    },
                    "status":i["status"]
                }
                data.append(data_group)    

            response = jsonify({ "data": data })
            # print(orderdata)
            return response
        response = jsonify({ "data": None })
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
@app.route("/history")
def history():
	return render_template("history.html")


if __name__=="__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
