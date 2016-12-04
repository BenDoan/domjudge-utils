import datetime
import json
import os
import re
import time

from os import path

import lib.bottle as bottle
from lib.bottle import *

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

USERNAME = "admin"
PASSWORD = "12345"

def check_auth(username, password):
    return username == USERNAME and \
            password == PASSWORD


@get('/<name:re:[@.A-Za-z0-9-_]+>')
@auth_basic(check_auth)
def index(name):
    with open("signout_times.csv", "a+") as f:
        f.write('{},{}\n'.format(name, int(time.time())))

    return '''<!DOCTYPE html><html><head></head>Good ({} {})<body>
	<audio autoplay> <source src="/static/A-Tone.wav" type="audio/wav"> </audio></body></html>'''.format(name, datetime.now())

# misc
@route('/static/<path:path>')
def static(path):
    return static_file(path, root=get_script_rel_path("static"))

@route('/A-Tone.wav')
def static(path):
    return static_file("A-Tone.wav")

def get_script_rel_path(filepath):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    return path.join(script_dir, filepath)


# remove ending slash from requests
@hook('before_request')
def strip_path():
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')

tpl_path = path.join(get_script_rel_path("templates"))
bottle.TEMPLATE_PATH.insert(0, tpl_path)

if __name__ == '__main__':
    run(host='0.0.0.0', port=12345)

app = default_app()
