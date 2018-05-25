

import json
import os
import random
import threading

import requests

import config as config


ISSUES = 'data'
COMMENTS = 'comments'
SELECTED = 'selected'
SELECTED_COMMENTS = 'selected_comments'
CLOSED = 'closed'

TIMEOUT = 5

for item in [ISSUES, COMMENTS, SELECTED, SELECTED_COMMENTS, CLOSED]:
    try:
        os.makedirs(item)
    except:
        pass


def fread(path):
    with open(path, 'rb') as file_handle:
        return file_handle.read()

def fwrite(path, data):
    with open(path, 'wb') as file_handle:
        if type(data)==str:
            data = data.encode()
        file_handle.write(data)


for item in os.listdir(ISSUES):
    print('Opening issue: '+ item.split('.')[0])
    data = fread(ISSUES + os.sep + item).decode()
    json_obj = json.loads(data)
    closed_by = ''
    if json_obj['state']=='closed':
        closed_by = json_obj['closed_by']['login']
    else:
        print('Issue: '+ item.split('.')[0] + ' not closed.')
        continue
    result = {}
    if json_obj['user']['login']==closed_by:
        result['body'] = json_obj
    else:
        result['body'] = {}
    
    result['comment'] = []

    try:
        comment_data = fread(COMMENTS + os.sep + item).decode()
    except:
        comment_data = None
    
    if comment_data:
        comment_json_obj = json.loads(comment_data)
        for comment_item in comment_json_obj:
            if comment_item['user']['login']==closed_by:
                result['comment'].append(comment_item)
            else:
                continue
    else:
        print('Issue ' + item.split('.')[0] + ' has no comment.')
    fwrite(CLOSED + os.sep + item, json.dumps(result))
