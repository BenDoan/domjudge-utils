#!/usr/bin/env python2
"""
This script creates a small web service that allows for remote account creation. Make sure to change the conn info in insert_user before using.

Requires: flask, MySQL-python

Assumptions: if bracket are used, the script assumes a 1400, 1620 and open team_category have been created

Example usage: curl --data "username=flasktest&password=password&token=acmsecret&bracket=open" bdo.pw:5000/user/add -X POST
"""

from flask import *
import sqlite3
import MySQLdb as mdb
import sys
import traceback

app = Flask(__name__)

contest_id_mapping = {
	"open": 7,
	"1620": 6,
	"1400": 5
}

TEAM_ROLE_ID = 3

def insert_user(username, password, bracket, name="NULL"):
    try:
        conn = mdb.connect('localhost', 'domjudge', 'testpass', 'domjudge')
        cur = conn.cursor()
        #cur.execute("SET FOREIGN_KEY_CHECKS=0")

        # find participant category
        cur.execute("SELECT * FROM team_category WHERE name='Participants'")
        cat = cur.fetchone()[0]

        # insert team
	insert_team_query = """INSERT INTO
	                        domjudge.team (teamid, externalid, name, categoryid, affilid, enabled, members, room, comments, judging_last_started, teampage_first_visited, hostname)
	                        VALUES (NULL, NULL, %s, %s, NULL, '1', NULL, NULL, NULL, NULL, NULL, NULL);"""
        cur.execute(insert_team_query, (username, cat))
        teamid = conn.insert_id()

        # insert user
	insert_user_query = """INSERT INTO
				domjudge.user (userid, username, name, email, last_login, last_ip_address, password, ip_address, enabled, teamid)
				VALUES (NULL, %s, %s, NULL, NULL, NULL, md5(%s),NULL, '1', %s);"""
	hashed_password = username + "#" + password
        cur.execute(insert_user_query, (username, name, hashed_password, teamid))
        userid = conn.insert_id()

        # insert user role
	insert_userrole_query = """INSERT INTO
				domjudge.userrole (userid, roleid)
				VALUES (%s, %s);"""
        cur.execute(insert_userrole_query, (userid, TEAM_ROLE_ID))

        # add team to contest
        contest_id = contest_id_mapping[bracket]
	insert_contestteam_query = """INSERT INTO
				domjudge.contestteam (cid, teamid)
				VALUES (%s, %s);"""
        cur.execute(insert_contestteam_query, (contest_id, teamid))

	conn.commit()
    except mdb.Error, e:
        traceback.print_exc()
        return "Error: %s" % e

    print "Added user {}:{} in bracket {}".format(username, name, bracket)

    return "Success"

@app.route('/user/add', methods=['POST'])
def user_add():
    if request.form.get("username") and request.form.get("password") and request.form.get("token") and request.form.get('name') and request.form.get('bracket'):
	if request.form.get("token") == "acmsecret":
	    return insert_user(request.form.get("username"),
	            request.form.get("password"),
	            name=request.form.get('name'),
	            bracket=request.form.get('bracket'))
	else:
	    print "Error: Invalid token"
            abort(418)
    else:
        print "Error: Invalid POST: {}".format(request.form)
        abort(418)

@app.route('/')
def hello():
    return "Hello"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
