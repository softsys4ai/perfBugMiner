
import os
import threading

from bs4 import BeautifulSoup

FOLDER = 'github_issues'
EXPORT_FOLDER = 'github_issues_exported'

try:
    os.mkdir(EXPORT_FOLDER)
except:
    pass

table = []
file_handles = {}

def get_labels(soup):
    result = []
    items = soup.find_all('div',  {'class': 'labels css-truncate'})
    if items!=[]:
        sub_items = items[0].find_all('a')
        for item in sub_items:
            result.append(item.text)
    return result

def get_title(soup):
    title_item = soup.select('#partial-discussion-header > div.gh-header-show > h1 > span.js-issue-title')
    if title_item:
        return title_item[0].text.strip()
    else:
        return ''

def get_content(soup, private_number):
    selector = '#issue-' + private_number + ' > div.edit-comment-hide > task-lists > table > tbody > tr > td'
    content_item = soup.select(selector)
    if content_item:
        return content_item[0].text.strip()
    else:
        return ''

def get_privte_number(soup):
    private_number_item = soup.find_all('meta', {'name': 'hovercard-subject-tag'})
    if private_number_item:
        return private_number_item[0]['content'].split(':')[-1]
    else:
        return '-1'

def covert_issue(file_name):
    item = file_name
    print('Issue: ' + item)
    if not item.isdigit():
        print('Item: ' + item + ' is not legal, ignore.')
        return
    if os.path.getsize(FOLDER + os.sep + item)==0:
        print('Item: ' + item + '\'size is 0, ignore.')
        return
    file_data = ''
    with open(FOLDER + os.sep + item, 'rb') as file_handle:
        file_data = file_handle.read().decode()
    soup = BeautifulSoup(file_data, 'html5lib')
    private_number = get_privte_number(soup)
    if private_number=='-1':
        print('File: ' + item + ': Get private number fail.')
        return
    labels = get_labels(soup)
    title = get_title(soup)
    content = get_content(soup, private_number)
    flag_performance = False
    for item in labels:
        if item.find('performance')!=-1:
            flag_performance = True
            break
    if content.find('performance')!=-1:
        flag_performance = True

    if flag_performance:
        label = 'performance'
    else:
        label = ''
        for item in labels:
            if item.find('type:')!=-1:
                label = item.replace('type:', '')
                break
        if label=='':
            label = 'no_label'
    
        issue_content = title
        issue_content+='\n\n'
        issue_content+=content
        table.append([label, issue_content])

for item in os.listdir(FOLDER):
    threading.Thread(target=covert_issue, args=(item,)).start()


for item in table:
    label = item[0]
    if label in file_handles:
        file_handle = file_handles[label]
    else:
        file_handle = open(EXPORT_FOLDER + os.sep + label + '.txt', 'wb')
        file_handles[label] = file_handle
    file_handle.write(item[1].encode())
    file_handle.write('\n\n*********************************************************************************\n\n'.encode())

for item in file_handles:
    file_handles[item].close()