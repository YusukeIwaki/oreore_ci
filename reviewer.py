# -*- coding:utf-8 -*-
from time import sleep
import json
import requests
import os

def review(pull_request_json):
    pull_request = json.loads(pull_request_json)

    repo_name = pull_request['base']['repo']['full_name']
    sha = pull_request['head']['sha']
    set_github_status(repo_name, sha, 'pending', 'now checking OREORE')
    
    # Pull Requestのチェックをいろいろやる
    check_coding_style(pull_request)
    try_building(pull_request)
    exec_acceptance_test(pull_request)
    
    set_github_status(repo_name, sha, 'success', 'OREORE: success')    

def set_github_status(repo_name, sha, status, description):
    data = {
        'state': status,
        'context': 'continuous-integration/oreore_ci',
        'description': description
    }
    url = 'https://api.github.com/repos/{repo_name}/statuses/{sha}'.format(repo_name=repo_name, sha=sha)
    requests.post(url, data=json.dumps(data), headers={'Authorization': 'token {token}'.format(token=os.environ['GITHUB_ACCESS_TOKEN'])})

def check_coding_style(pull_request):
    sleep(3)

def try_building(pull_request):
    sleep(10)

def exec_acceptance_test(pull_request):
    sleep(4)
