#!/usr/bin/env python2

from flask import *
import sqlite3
import MySQLdb as mdb
import sys

app = Flask(__name__)

def insert_user(username, password, name="NULL", email="NULL"):
    try:
        conn = mdb.connect('localhost', 'admin', 'changemepass', 'domjudge')
        cur = conn.cursor()

        hashed_password = username + "#" + password

        cur.execute("INSERT INTO domjudge.user (userid, username, name, email, last_login, last_ip_address, password, ip_address, enabled, teamid) VALUES (NULL, {}, {}, md5({}), NULL, NULL, {}, NULL, '1', NULL);".format(username, name, email, hashed_password))
    except mdb.Error, e:
        return "Error"

    print "Success"

@app.route('/user/add', methods=['POST'])
def hello_world():
    if request.form.get("username") request.form.get("password"):
        return insert_user(request.form.get("username"), request.form.get("password"))
    else:
        abort(418)

if __name__ == '__main__':
    app.run()
