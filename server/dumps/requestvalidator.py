from flask import request
import json, hashlib, time
def login_request_validator(func):
    def inner_wrapper():
        responseDict = {
            "statusCode" : "",
            "description": ""
        }
        if(request.is_json == False or request.method != "POST"):
            responseDict['statusCode'] = 404
            responseDict['description'] = "Bad request Format"
            return responseDict
        else:
            return func()   
    return inner_wrapper

def registration_request_validator(mysql):
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
    
    return  json.dumps(responseDict)