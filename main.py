from flask import request, jsonify
from flask import Flask
import sqlite3
from flaskext.mysql import MySQL
import json
app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sportsclub'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()


def delete(query):
    print("delete")
    try:
        cursor.execute(query)
        conn.commit()
        return True
    except Exception as e:
        print("Problem Deleting from db: " + str(e))
        return False


def insert(query):
    print("insert")
    try:
        cursor.execute(query)
        conn.commit()
        return True
    except Exception as e:
        print("Problem inserting into db: " + str(e))
        return False


def select(query):
    print("select")
    cursor.execute(query)
    table = cursor.fetchall()
    print(json.dumps(table))
    return table


def user_exists(username):
    for row in select("SELECT username FROM user"):
        if username == row[0].lower():
            return True
    return False


def valid_user(username, password):
    for row in select("SELECT username,password,type FROM user"):
        if username == row[0] and password == row[1]:
            return True, row[2]
    return False, row[2]


@app.route('/login', methods=["POST"])
def login():
    json = request.get_json()
    status = {"message": "Invalid Credentials", "code": 302, "type": "user"}
    print(json)
    try:

        if request.method == "POST":
            username = str(json['username']).strip().lower()
            password = str(json['password']).strip()

            isValid, utype = valid_user(username, password)

            if isValid:
                status['message'] = "Valid User"
                status['code'] = 200
                status['type'] = utype
            return jsonify(status)
        return jsonify({"message": "Invalid Request"})
    except Exception:
        return jsonify({"error": "Try Again Later"})


@app.route('/signup', methods=["POST"])
def signup():
    json = request.get_json()
    status = {'message': "Could Not Complete Request", 'code': 302}
    print(json)
    try:

        if request.method == "POST":
            username = str(json['username']).strip().lower()
            password = str(json['password']).strip()
            mail = str(json['mail']).strip().lower()
            mobile = str(json['mobile']).strip().lower()

            if user_exists(username):
                status['message'] = "Username Already Exists"
                status['code'] = 200
            else:
                query = "insert into  user(userid, username, password, type, email, mobile) values('{}','{}','{}','{}','{}','{}')".format(
                        '0', username, password, 'user', mail, mobile)
                print(query)
                if insert(query):
                    status['message'] = "Signup is Successful"
                    status["code"] = 200
            return jsonify(status)
    except Exception:
        return jsonify({"error": "Try Again Later"})


@app.route('/deleteAccount', methods=["POST"])
def deleteAccount():
    json = request.get_json()
    status = {"message": "Problem while Deleting you account",
              "code": 302, "type": "user"}
    print(json)
    try:
        if request.method == "POST":
            username = str(json['username']).strip().lower()
            query = "delete from user where username='{}'".format(username)
            print(query)
            if delete(query):
                status['message'] = "Sucessfully Deleted Account"
                status['code'] = 200

            return jsonify(status)
        return jsonify({"message": "Invalid Request"})
    except Exception:
        return jsonify({"error": "Try Again Later"})


@app.route('/getSportsList', methods=["POST"])
def getSportsList():
    result = select("select * from sports")

    status = {"message":  json.dumps(result),
              "code": 200}
    return status


@app.route('/addSports', methods=["POST"])
def addSport():
    json = request.get_json()
    sportname = str(json['sportname']).strip().lower()
    cost = str(json['cost']).strip().lower()

    status = {"message":  "Problem While Adding Sport",
                          "code": 200}

    query = "insert into  sports values('{}','{}','{}')".format(
        '0', sportname, cost)
    if insert(query):
        status['message'] = "Added Sport"
        status["code"] = 200
    return status


@app.route('/removeSports', methods=["POST"])
def removeSport():
    json = request.get_json()
    sportsid = str(json['sportsid']).strip().lower()

    status = {"message":  "Problem While Removing Sport",
                          "code": 200}

    query = "delete from sports where sportsid='{}'".format(sportsid)

    if delete(query):
        status['message'] = "Removed Sport"
        status["code"] = 200
    return status

@app.route('/getStaffList', methods=["POST"])
def getStaffList():
    result = select("select * from staff")

    status = {"message":  json.dumps(result),
              "code": 200}
    return status


@app.route('/addStaff', methods=["POST"])
def addStaff():
    json = request.get_json()
    staffname = str(json['staffname']).strip().lower()
    sportsid = str(json['sportsid']).strip().lower()

    status = {"message":  "Problem While Adding Staff",
                          "code": 200}

    query = "insert into  staff values('{}','{}','{}')".format(
        '0', staffname, sportsid)
    
    if insert(query):
        status['message'] = "Added Staff"
        status["code"] = 200
    return status


@app.route('/removeStaff', methods=["POST"])
def removeStaff():
    json = request.get_json()
    staffid = str(json['staffid']).strip().lower()

    status = {"message":  "Problem While Removing Staff",
                          "code": 200}

    query = "delete from staff where staffid='{}'".format(staffid)

    if delete(query):
        status['message'] = "Removed Sport"
        status["code"] = 200
    return status


if __name__ == '__main__':
    app.run(host="0.0.0.0")
