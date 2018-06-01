

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
EXPORT = 'export'


TIMEOUT = 5

for item in [ISSUES, COMMENTS, SELECTED, SELECTED_COMMENTS, CLOSED, EXPORT]:
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

handles = {}

for item in os.listdir(ISSUES):
    print('Opening issue: '+ item.split('.')[0])
    data = fread(ISSUES + os.sep + item).decode()
    json_obj = json.loads(data)
    is_performance = False
    for label_item in json_obj.get('labels', {}):
        if 'performance' in label_item['name']:
            is_performance = True
    if 'performance' in json_obj['title'] + json_obj['body']:
        is_performance = True
    type_ = ''
    for lable_item in json_obj.get('labels', {}):
        if lable_item['name'].startswith('type:'):
            type_ = lable_item['name'].split(':')[-1].replace('/', '_')
            break
    if type_=='':
        continue
    handle = handles.get(type_, open(EXPORT + os.sep + type_, 'a+b'))
    buffer = ''
    buffer+=json_obj['title']
    buffer+='\n'
    buffer+=json_obj['body']
    buffer+='\n'
    for lable_item in json_obj.get('labels', {}):
        buffer+=lable_item['name']
        buffer+='\n'
    buffer+='???timeline???'
    buffer+='\n'
    try:
        data = fread(ISSUES + os.sep + item).decode()
        json_obj = json.loads(data)
        for comment_item in json_obj:
            buffer+=json_obj['user']['login']
            buffer+='\n'
            buffer+='???character???'
            buffer+='\n'
            buffer+=json_obj['body']
            buffer+='\n'
    except:
        print('ERROR.....................')
    handle.write(buffer.encode())
    handle.flush()
    if(is_performance):
        print(item)
        handle = open(EXPORT + os.sep + item, 'wb')
        handle.write(buffer.encode())
        handle.close()