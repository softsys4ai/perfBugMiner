
import atexit
import json
import os
import random
import threading

import requests

import config as config


URL_BASE = 'https://api.github.com'
RETRY_MAX = 3


class Github:

    owner = None
    repositorie = None
    client_id = None
    client_secret = None

    #session = {}

    def __init__(self, owner, repositorie, client_id, client_secret):
        self.owner = owner
        self.repositorie = repositorie
        self.client_id = client_id
        self.client_secret = client_secret

    def get_url(self, target, args):
        args_list = []
        for item in (self.owner, self.repositorie, ):
            args_list.append(item)
        for item in args:
            args_list.append(item)
        if False:
            pass
        elif target=='issues':
            url = URL_BASE + '/repos/%s/%s/issues' % tuple(args_list)
        elif target=='comment':
            url = URL_BASE + '/repos/%s/%s/issues/%s/comments' % tuple(args_list)
        elif target=='issue':
            url = URL_BASE + '/repos/%s/%s/issues/%s' % tuple(args_list)
        else:
            pass
        return url
    
    #def get_session(self):
    #    return ''.join(random.sample(string.ascii_letters + string.digits, 8))

    def get(self, url, params):
        try:
            return requests.get(url, params=params, timeout=TIMEOUT)
        except Exception as exception:
            print('ERROR:', exception)
            return None

    def get_comment(self, number):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        respon = self.get(self.get_url('comment', [str(number)]), params)
        if respon:
            return respon.content
        else:
            print('ERROR:', respon.status_code, respon.content)
            return None

    def get_a_single_issue(self, number):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        respon = self.get(self.get_url('issue', [str(number)]), params)
        if respon:
            return respon.content
        else:
            print('ERROR:', respon.status_code, respon.content)
            return None

    def get_issues(self, page=None, filter_=None, state=None):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        if page:
            params['page'] = page
        if filter_:
            params['filter'] = filter_
        if state:
            params['state'] = state
        respon = self.get(self.get_url('issues', []), params)
        if respon:
            return respon.content
        else:
            print('ERROR:', respon.status_code, respon.content)
            return None


ISSUES = 'data'
COMMENTS = 'comments'
SELECTED = 'selected'
SELECTED_COMMENTS = 'selected_comments'

TIMEOUT = 5

for item in [ISSUES, COMMENTS, SELECTED, SELECTED_COMMENTS]:
    try:
        os.makedirs(item)
    except:
        pass

def pretty_json(json_object):
    return json.dumps(json_object, indent=4)

def fwrite(path, data):
    with open(path, 'wb') as file_handle:
        if type(data)==str:
            data = data.encode()
        file_handle.write(data)

def async_fwrite(path, data):
    t = threading.Thread(target=fwrite, args=(path, data, ))
    t.start()

github = Github(config.owner, config.repositorie, config.client_id, config.client_secret)



def hook_writing_issues(object_):
    temp_text = object_['title'] + object_['body']
    for item in object_['labels']:
        temp_text+=item['name']
    if 'performance' in temp_text.lower():
            path = SELECTED + os.sep + str(object_['number']).zfill(6) + '.json'
            async_fwrite(path, pretty_json(object_))
            return True
    
    return False


def hook_writing_issues_comment(object_):
    temp_text = object_['title'] + object_['body']
    for item in object_['labels']:
        temp_text+=item['name']
    if 'performance' in temp_text.lower():
            path = SELECTED + os.sep + str(object_['number']).zfill(6) + '.json'
            async_fwrite(path, pretty_json(object_))


def hook_writing_issue_comments(object_, number, flag):
    if flag:
            path = SELECTED_COMMENTS + os.sep + str(number).zfill(6) + '.json'
            async_fwrite(path, pretty_json(object_))

retry = 0



number = 19498

while True:

    flag = False

    respon = github.get_a_single_issue(number)
    print('Getting issue:' + str(number))
    if respon:
        json_object = json.loads(respon)
        path = ISSUES + os.sep + str(number).zfill(6) + '.json'
        async_fwrite(path, pretty_json(json_object))
        flag = hook_writing_issues(json_object)
        print(flag)
        retry = 0
    else:
        retry+=1
        if retry>RETRY_MAX:
            print('Can\'t download issue: ' + str(number));
            retry = 0
            number+=1
            continue
    
    respon = github.get_comment(number)
    print('Getting issue comments:' + str(number))
    if respon:
        json_object = json.loads(respon)
        path = COMMENTS + os.sep + str(number).zfill(6) + '.json'
        async_fwrite(path, pretty_json(json_object))
        hook_writing_issue_comments(json_object, number, flag)
        retry = 0
        number+=1
    else:
        retry+=1
        if retry>RETRY_MAX:
            print('Can\'t download issue\'s comments: ' + str(number));
            retry = 0
            number+=1
            continue


