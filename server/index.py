from flask import Flask
from flask import request
from flask_mysqldb import MySQL
import hashlib
import json
import time
app = Flask(__name__)
# @app.route("/")
# pass
json_file = ""
try:
    json_file = json.load(open("connection.json","r"))
    print("file load Successful")
except Exception as e:
    print("File loading error: ",e)
app.config["MYSQL_HOST"] = json_file["host"]
app.config["MYSQL_USER"] = json_file["user"]
app.config["MYSQL_PASSWORD"] = json_file["password"]
app.config["MYSQL_DB"] = json_file["database"]
mysql = MySQL(app)

@app.route("/user/register",methods = ["POST"])
def register_user():
    # print(request.is_json)
    # print(request.get_json())
    responseDict = {
        "statusCode" : "",
        "description": ""
    }
    json_data = request.get_json()
    email_id = json_data['email_id']
    sql = "SELECT * FROM students WHERE email_id = '"+email_id+"'"
    rows = 0
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        if(len(rows) > 0):
            responseDict['statusCode'] = 205
            responseDict['description'] = "Student Already Exists"
        #print("Rows",len(rows))
        # responseDict['statusCode'] = 205
        # responseDict['description'] = "Student Already Exists"
    except Exception as e:
        print("Checking error: ",e)
        responseDict['statusCode'] = 404
        responseDict['description'] = "Exception Occured"
    finally:
        cursor.close()
    if(len(rows) > 0):
        return json.dumps(responseDict)

    student_id = str(int(time.time()))
    first_name = json_data['f_name']
    last_name = json_data['l_name']
    phone_number = json_data['phno']
    permanent_address = json_data['address1']
    local_address = json_data['address2']
    password = hashlib.md5(json_data['password'].encode())
    sql = "INSERT INTO students VALUES ('"+student_id+"','"+first_name+"','"+last_name+"','"+phone_number+"','"+email_id+"','"+permanent_address+"','"+local_address+"','"+str(password.hexdigest())+"')"
    cursor = mysql.connection.cursor()
    print(cursor)
    try:
        cursor.execute(sql)
        cursor.connection.commit()
        responseDict['statusCode'] = 200
        responseDict['description'] = "Success"
    except Exception as e:
        print("SQL Error: ",e)
        responseDict['statusCode'] = 404
        responseDict['description'] = str(e)
    finally:
        cursor.close()
    
    return  json.dumps(responseDict)

@app.route("/user/login",methods = ["POST"])
def login_user():
    json_data = request.get_json()
    print(json_data)
    user_id = json_data['user_id'] if "user_id" in json_data else ""
    password = json_data['password'] if "password" in json_data else ""
    print(user_id+" "+password)
    
if(__name__ == "__main__"):
    app.run(debug = True)