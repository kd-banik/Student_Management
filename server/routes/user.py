from flask import Blueprint, request, make_response,redirect,url_for
from extension.extension import mysql,session
import json, hashlib, time
from flask_cors import CORS
user = Blueprint("user",__name__)
CORS(user)
@user.route("/index",methods = ['GET'])
def index():
    message = None
    if('user_name' in session):
        message = "You are logged in"
    else:
        message = "Please login first"
    return message

@user.route("/login",methods = ["POST"])
def login():
    responseDict = {
            "statusCode" : "200",
            "description": "Succcess login"
        }
    if('email_id' in session and 'student_id' in session):
        responseDict['statusCode'] = 200
        responseDict['description'] = "You are already Logged in"
        return responseDict

    if(request.is_json == False or request.method != "POST"):
        responseDict['statusCode'] = 404
        responseDict['description'] = "Bad request Format"
        return responseDict
    json_data = request.get_json()
    print("Request Data: ",json_data)
    print("Request Cookies: ",request.cookies.get('user_id'))
    user_id = json_data['user_id'] if "user_id" in json_data else ""
    password = json_data['password'] if "password" in json_data else ""
    if(user_id == "" or password == ""):
        responseDict['statusCode'] = 404
        responseDict['description'] = "Bad request Format"
        return responseDict
    encodedPassword = hashlib.md5(password.encode()).hexdigest()
    cursor = mysql.connection.cursor()
    rows = 0
    sql = "SELECT student_id,email_id,first_name,last_name,password FROM students WHERE email_id = '"+user_id+"'"
    rowdata = ""
    cookie_string = None
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        rowdata = dict(student_id = str(rows[0][0]),email_id = str(rows[0][1]),first_name = str(rows[0][2]), last_name = str(rows[0][3]))
        user_pass_db = str(rows[0][4])
    except Exception as e:
        print(e)
        responseDict['statusCode'] = 404
        responseDict['description'] = "Exception Occured"
    finally:
        cursor.close()
    if(len(rows) <= 0):
        responseDict['statusCode'] = 405
        responseDict['description'] = "User Not found"
    elif(len(rows) == 1 and encodedPassword != user_pass_db):
        responseDict['statusCode'] = 406
        responseDict['description'] = "Wrong password"
    else:
        responseDict['statusCode'] = 200
        responseDict['description'] = "SuccessFul"
        session['email_id'] = rowdata['email_id']
        session['student_id'] = rowdata['student_id']
        cookie_string = hashlib.md5(user_id.encode()).hexdigest()
    response = make_response(json.dumps(responseDict))
    response.set_cookie('user_id',cookie_string)
    return response

@user.route("/register",methods = ["POST"])
def registration():
    responseDict = {
        "statusCode" : "200",
        "description": "Success Registration"
    }
    if('email_id' in session):
        responseDict['statusCode'] = 200
        responseDict['description'] = "You are already Logged in"
        return responseDict
    
    # responseDict['appContext'] = has_app_context()
    # print("App context: ",responseDict['appContext'])
    json_data = request.get_json()
    email_id = json_data['email_id']
    sql = "SELECT * FROM students WHERE email_id = '"+email_id+"'"
    rows = 0
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Exception as e:
        print("Checking error: ",e)
        responseDict['statusCode'] = 404
        responseDict['description'] = "Exception Occured"
    finally:
        cursor.close()
    if(len(rows) > 0):
        responseDict['statusCode'] = 205
        responseDict['description'] = "Student Already Exists"
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
    return  responseDict

@user.route("/logout",methods = ['GET'])
def logout():
    message = None
    if('email_id' in session and 'student_id' in session):
        session.pop('email_id',None)
        session.pop('student_id',None)
        message = "SuccessFully Logged out"
    else:
        message = "you are not logged in"
    return redirect(url_for('index'))
