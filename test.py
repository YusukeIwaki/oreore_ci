# -*- coding:utf-8 -*-

from bottle import Bottle, run, request, response
from pprint import pprint
import os,sys
import hashlib
import hmac
from rq import Queue
from worker import conn
from reviewer import review
import json

app = Bottle()

@app.post('/event_handler')
def handle_event():
    if not verify_signature(request.get_header('X-Hub-Signature'), request.body.read()):
        response.status = 400
        response.body = 'bad request'
        return response

    payload = request.json
    event_name = request.get_header('X-GitHub-Event')
    if event_name == 'pull_request':
        if payload['action'] == 'opened' or payload['action'] == 'reopened':
            return handle_pull_request_created(payload['pull_request'])
        elif payload['action'] == 'synchronize':
            return handle_pull_request_updated(payload['pull_request'])
    elif event_name == 'pull_request_review_comment':
        if payload['action'] == 'created':
            return handle_pull_request_comment_created(payload['comment'])
        elif payload['action'] == 'edited':
            return handle_pull_request_comment_edited(payload['comment'])
    elif event_name == 'issue_comment':
        if payload['action'] == 'created':
            return handle_pull_request_comment_created(payload['comment'])
        elif payload['action'] == 'edited':
            return handle_pull_request_comment_edited(payload['comment'])

    return '<b>Hello</b>!'

def verify_signature(signature, payload):
    if signature:
        return signature == "sha1="+hmac.new(b'okighoo9eez9eivahQu0ugoishoh2Lah', payload, hashlib.sha1).hexdigest()
    else:
        return False

def handle_pull_request_created(pull_request):
    pprint(pull_request)
    return 'ok: created'

def handle_pull_request_updated(pull_request):
    pprint(json.dumps(pull_request))
    Queue(connection=conn).enqueue(review, json.dumps(pull_request))
    return 'ok: updated'

def handle_pull_request_comment_created(comment):
    pprint(comment)
    return 'ok: comment created'

def handle_pull_request_comment_edited(comment):
    pprint(comment)
    return 'ok: comment edited'

port = os.getenv('PORT', 80) if len(sys.argv)<2 else int(sys.argv[1])
run(app, host='0.0.0.0', port=port)
