#!/usr/bin/env python2
"""
This script creates a small web service that allows for remote account creation. Make sure to change the conn info in insert_user before using.

Requires: flask, MySQL-python

Example usage: curl --data "username=flasktest&password=password&token=acmsecret" bdo.pw:5000/user/add -X POST
"""

from flask import *
import sqlite3
import MySQLdb as mdb
import sys

app = Flask(__name__)

def insert_user(username, password, name="NULL", email="NULL"):
    try:
        conn = mdb.connect('localhost', 'root', 'testpass', 'domjudge')
        cur = conn.cursor()

	hashed_password = username + "#" + password

	insert_user_query = """INSERT INTO 
				domjudge.user (userid, username, name, email, last_login, last_ip_address, password, ip_address, enabled, teamid) 
				VALUES (NULL, %s, %s, %s, NULL, NULL, md5(%s),NULL, '1', '4');"""

        cur.execute(insert_user_query, (username, name, email, hashed_password))
	conn.commit()
    except mdb.Error, e:
        return "Error: %s" % e

    return "Success"

@app.route('/user/add', methods=['POST'])
def hello_world():
    if request.form.get("username") and request.form.get("password") and request.form.get("token") and request.form.get('name'):
	if request.form.get("token") == "acmsecret":
	    return insert_user(request.form.get("username"), request.form.get("password"), name=request.form.get('name'))
	else:
	    print "Error: Invalid token"
            abort(418)
    else:
        print "Error: Invalid POST: {}".format(request.form)
        abort(418)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
