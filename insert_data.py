import pymysql
import json

with open('taipei-day-trip-website/data/taipei-attractions.json',encoding='UTF-8') as f:
    data = json.load(f)
data = data['result']
conn = pymysql.connect(host='localhost',user='root',password='rootroot',db='daytrip',charset='utf8')
cur = conn.cursor()

for d in data.get('results'):
    id = d.get('_id')
    name = d.get('name')
    category = d.get('CAT')
    description = d.get('description')
    address = (d.get('address').replace(" ", ""))
    transport = d.get('direction').replace("&nbsp;", " ")
    mrt = d.get('MRT')
    lat = d.get('latitude')
    lng = d.get('longitude')
    image = d.get('file').lower().replace(".jpg",".jpg,").split(",")[:-1]
    s = ', '
    images = s.join(image)

    sql_insert = "INSERT INTO attraction(id, name, category, description, address, transport, mrt, lat, lng, images)VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" 
    params_insert = (id, name, category, description, address, transport, mrt, lat, lng, images)

    try:
        cur.execute(sql_insert, params_insert)   
        conn.commit() 
    except:
        conn.rollback()

conn.close()