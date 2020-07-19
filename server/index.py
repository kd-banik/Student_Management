from flask import Flask ,g
from flask import request
from extension.extension import mysql
from routes.user import user
from routes.blog import blog
import hashlib
import json
import time
#from routes.user import user
app = Flask(__name__)
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
mysql.init_app(app)
app.register_blueprint(user,url_prefix = "/user")
"""
/user/login
/user/register
"""
app.register_blueprint(blog,url_prefix = "/blog")
"""
/blog/post
/blog/modify
/blog/get
"""

if(__name__ == "__main__"):
    app.run(debug = True)