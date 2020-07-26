from flask import Blueprint, request, url_for, redirect
from extension.extension import mysql, session
import json , time, hashlib
from flask_cors import CORS
blog = Blueprint("blog",__name__)
CORS(blog)

@blog.route("/post", methods = ["POST"])
def submit_post():
    responseDict = {
        "statusCode" : 200,
        "description" : "Success"
    }
    if('email_id' not in session and 'student_id' not in session):
        return redirect(url_for('user.index'))
    
    if(request.is_json == False or request.method != "POST"):
        responseDict = {
            "statusCode" : 404,
            "description" : "Bad Request Format"
        }
        return json.dumps(responseDict)
    blog_data = request.get_json()
    blog_title = blog_data['blog_title'] if "blog_title" in blog_data else ""
    blog_content = blog_data['blog_content'] if "blog_content" in blog_data else ""
    blog_student_id = blog_data['student_id'] if "student_id" in blog_data else ""
    if(blog_title == "" or blog_content == "" or blog_student_id == ""):
        responseDict['statusCode'] = 404
        responseDict['description'] = "Bad Request Data"
        return json.dumps(responseDict)
    blog_id = str(int(time.time()))
    blog_slug = blog_id + blog_title + blog_student_id
    sql = "INSERT INTO student_blog_post VALUES ('{}','{}','{}','{}','{}')".format(blog_id,blog_slug,blog_title,blog_content,blog_student_id)
    sql_flag =  1
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        mysql.connection.commit()
    except Exception as e:
        print("BLOG POST SQL: ",e)
        sql_flag = 0
    finally:
        cursor.close()
    if(sql_flag == 0):
        responseDict = {
            "statusCode": 404,
            "description": "SQL exception error"
        }
        return json.dumps(responseDict)
    return json.dumps(responseDict)


@blog.route("/modify", methods = ["PUT","DELETE"])
def modify_blog():
    responseDict = {
        "statusCode": 405,
        "description": "Unknown"}
    blog_data_modify = None
    if('email' not in session and 'student_id' not in session):
        return redirect(url_for('user.index'))
    
    if(request.is_json):
        blog_data_modify = request.get_json()
    else:
        responseDict["statusCode"] = 404
        responseDict["description"] = "Bad Request Data"
        return responseDict

    if(session['student_id'] != blog_data_modify['student_id']):
        responseDict["statusCode"] = 406
        responseDict["description"] = "access Violation"
        return responseDict
    elif(request.method == "PUT" and "blog_id" not in blog_data_modify and "blog_content" not in blog_data_modify and "student_id" not in blog_data_modify and "blog_title" not in blog_data_modify):
        responseDict["statusCode"] = 404
        responseDict["description"] = "Bad Request Data"
        return responseDict
    elif(request.method == "DELETE" and "blog_id" not in blog_data_modify and "student_id" not in blog_data_modify):
        responseDict["statusCode"] = 404
        responseDict["description"] = "Bad Request Data"
        return responseDict
    sql = None
    if(request.method == "PUT"):
        new_slug = blog_data_modify['blog_id'] + blog_data_modify['blog_content'] + blog_data_modify['student_id']
        sql = "UPDATE student_blog_post SET blog_title = '{}',blog_content = '{}',blog_slug = '{}' WHERE blog_id = '{}' AND student_id = '{}'".format(blog_data_modify['blog_title'],blog_data_modify['blog_content'],new_slug,blog_data_modify['blog_id'],blog_data_modify['student_id'])
    elif(request.method == "DELETE"):
        sql = "DELETE FROM student_blog_post WHERE student_id = '{}' AND blog_id = '{}'".format(blog_data_modify['student_id'],blog_data_modify['blog_id'])
    mysql_flag = True
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        mysql.connection.commit()
    except Exception as e:
        print("SQL Exception",e)
        responseDict['statusCode'] = 405
        responseDict['description'] = "SQL Exception Occured"
        mysql_flag = False
    finally:
        cursor.close()
    if(mysql_flag == False):
        return json.dumps(responseDict)
    else:
        responseDict['statusCode'] = 200
        responseDict['description'] = "Success"
    return json.dumps(responseDict)

@blog.route("/get",methods = ["GET"])
def get_blog():
    responseDict = {
        "statusCode": 404,
        "description": "Error in Sql"
    }
    sql = "SELECT * FROM student_blog_post"
    sql_flag = 1
    blog_data = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        mysql.connection.commit()
        blog_data = cursor.fetchall()
    except Exception as e:
        print("Get Blog Error: "+e)
        sql_flag = 0
    finally:
        cursor.close()
    if(sql_flag == 0):
        return json.dumps(responseDict)
    new_rows = tuple((x,blog_data[0]) for x in range(0,len(blog_data)))
    print("new rows: ",new_rows)
    new_blog_rows = dict(new_rows)
    return new_blog_rows

@blog.route("/get/<int:id>",methods = ["GET"])
def get_blog_by_id(id):
    responseDict = {
        "status": 404,
        "description":"Error"
    }
    blog_id = id
    sql = "SELECT * FROM student_blog_post WHERE blog_id = '{}'".format(blog_id)
    result = None
    sqlFlag = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        mysql.connection.commit()
    except Exception as e:
        print("fetching blog by id sql error: ",e)
        sqlFlag = True
    finally:
        cursor.close()
    #print(result)
    if(sqlFlag):
        return json.dumps(responseDict)
    elif(len(result)<=0):
        responseDict = {"statusCode":"205","description":"Now blog found"}
        return json.dumps(responseDict)
    return json.dumps(result)
    