def update_blog(blog_id,blog_title,blog_content,blog_student_id, mysql):
    responseDict = {
        'statusCode': 200,
        'description': 'Success'
    }
    blog__id = blog_id
    blog__title = blog_title
    blog__content = blog_content
    blog__student__id = blog_student_id
    if(blog__id == "" or blog__title == "" or blog__content == "" or blog__student__id == ""):
        responseDict['statusCode'] = 404
        responseDict['description'] = "Bad Request Data"
        return responseDict
    
    blog__slug = blog__id + blog__title + blog__student__id
    sql = "UPDATE student_blog_post SET blog_title = '{}',blog_content = '{}',blog_slug = '{}' WHERE blog_id = '{}' AND student_id = '{}'".format(blog__title,blog__content,blog__slug,blog__id,blog__student__id)
    mysql_flag = 1
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        mysql.connection.commit()
    except Exception as e:
        print("Update SQL ERROR: ",e)
        mysql_flag = 0
    finally:
        cursor.close()
    if(mysql_flag == 0):
        responseDict['statusCode'] = 404
        responseDict['description'] = "SQL Exception error"
    return responseDict

def delete_blog(blog_id,blog_student_id,mysql):
    responseDict = {
        "statusCode" : 200,
        "description": "Success"
    }
    blog__id = blog_id
    blog__student__id = blog_student_id
    if(blog__id == "" or blog__student__id == ""):
        responseDict['statusCode'] = 404
        responseDict['description'] = "Bad Data Request"
        return responseDict
    sql = "DELETE FROM student_blog_post WHERE blog_id = '{}' AND student_id = '{}'".format(blog__id,blog__student__id)
    mysql_flag = 1
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        mysql.connection.commit()
    except Exception as e:
        print("DELETE EXCEPTION ERROR: ",e)
        mysql_flag = 0
    finally:
        cursor.close()
    if(mysql_flag == 0):
        responseDict['statusCode'] = 404
        responseDict['description'] = "SQL Exception ERROR"
    return responseDict