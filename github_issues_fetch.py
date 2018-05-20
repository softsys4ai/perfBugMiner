
PROJECT_URL_BASE = 'https://github.com/tensorflow/tensorflow'
FOLDER = 'github_issues'

#https://github.com/tensorflow/tensorflow/issues/19296

import os
import random
import time
import socket

import requests

from bs4 import BeautifulSoup

class DummyRespon:

    status_code = 0

    def __init__(self):
        pass

socket.setdefaulttimeout(8)

try:
    os.mkdir(FOLDER)
except:
    pass

raw_file_list = os.listdir(FOLDER)

next_issue_number = 1

if raw_file_list==[]:
    next_issue_number = 1
else:
    for item in raw_file_list:
        try:
            if int(item)>next_issue_number:
                next_issue_number = int(item)
            else:
                pass
        except:
            pass
    next_issue_number+=1

#type:bug/performance

flag_exit = False
status_code_404_count = 0
last_accessible_issue = -1
max_issue_number = -1

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
}


while max_issue_number==-1:
    try:
        respon = requests.get(PROJECT_URL_BASE + '/issues', headers=headers)
        if respon:
            content = respon.content
            soup = BeautifulSoup(content, 'html5lib')
            html_block = soup.select('#js-repo-pjax-container > div.container.new-discussion-timeline.experiment-repo-nav > div.repository-content > div > div.border-right.border-bottom.border-left > ul')
            max_issue_number = int(html_block[0].li['id'].split('_')[-1])
        else:
            status_code_404_count+=1
        if status_code_404_count>=5:
            print('Can\' t get max issue number. Program will exit.')
            exit(-1)
    except:
        pass

status_code_404_count = 0


while not flag_exit:
    url = PROJECT_URL_BASE + '/issues/' + str(next_issue_number)
    try:
        respon = requests.get(url, headers=headers)
    except:
        respon = DummyRespon()
    if respon:
        print('Issue: ' + str(next_issue_number) + ': Fetch success.')
        path = FOLDER + os.sep + str(next_issue_number)
        with open(path, 'wb') as file_handle:
            file_handle.write(respon.content)
        last_accessible_issue = next_issue_number
    else:
        print('Issue: ' + str(next_issue_number) + ': Fetch error, status_code: ' + str(respon.status_code))
    if next_issue_number>max_issue_number:
        print('Got all issues, exit.')
    next_issue_number+=1
    duration = int(random.random() * 10) % 3
    print('Sleep: ' + duration)
    time.sleep(duration)
