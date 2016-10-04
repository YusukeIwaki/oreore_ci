# -*- coding:utf-8 -*-

from bottle import Bottle, run, request
from pprint import pprint

app = Bottle()

@app.post('/event_handler')
def handle_event():
    pprint(request)
    return '<b>Hello</b>!'

run(app, host='localhost', port=80)
