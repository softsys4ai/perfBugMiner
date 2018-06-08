# -*- coding: utf-8 -*-
from config import *
import json
import csv
import time
titles = []

# csvFile = open(ClosedFile,'w')
# writer = csv.writer(csvFile)
def save(it):
    csvfile = open(ClosedFile, 'ab+')
    writer = csv.writer(csvfile)
    writer.writerow(it)
    csvfile.close()

def getComments(url):
    content = GetJsonFromAPI(url)
    if content is None:
        return []
    js = json.loads(content)
    comments = []
    for comment in js:
        item = {}
        item['body'] = comment['body']#.replace("\n",'')
        item['author_association'] = comment['author_association']
        item['created_at'] = comment['created_at']
        item['updated_at'] = comment['updated_at']
        comments.append(item)
    return comments

def SaveHeader():
    csvFile = open(ClosedFile,'wb')
    writer = csv.writer(csvFile)
    h=[]
    h.append("ISSUE TITLE")
    h.append("ISSUE`S LABEL")
    h.append("ISSUE`S CREATED TIME")
    h.append("ISSUE`S UPDATED TIME")
    h.append("ISSUE`S CLOSED TIME")
    h.append("ISSUE DESCRIPTION")
    h.append("CHARACTER OF THE USER WHO CLOSED THE ISSUE")
    h.append("COMMENT OF THE USER WHO CLOSED THE ISSUE")
    for i in range(1,40):
        h.append(str(i)+"th COMMENT")
        h.append(str(i)+"th COMMENT`S USER CHARACTER")
    writer.writerow(h)
    csvFile.close()

SaveHeader()

page = 1

MaxCommentNum = 0

while True:
    url = baseurl + "?page="+str(page)+"&state=closed"+"&"+urlend
    page +=1
    print u"EXTRACTING:",url
    content = GetJsonFromAPI(url)
    if content is None:
        break
    js = json.loads(content)
    for item in js:
        it = []
        comments_url = item['comments_url']
        time.sleep(TIMEOUT)
        comments = []
        closed_user = item['author_association']
        closed_commemt = ''
        closed_at = item['closed_at']
        title = item['title'].encode("utf-8")
        labels = json.dumps(item['labels'])
        labels = labels.encode("utf-8")
        body = item['body'].encode('utf-8')
        if "type:bug/performance" not in labels.lower() and  keyword not in title.lower() and keyword not in body.lower():
            continue
        if title in titles:
            continue
        titles.append(title)
        if item['comments'] is not 0:
            comments = getComments(comments_url+"?"+urlend)
            for temp in comments:
                if temp['created_at']==closed_at or temp['updated_at'] == closed_at:
                    closed_user=temp['author_association']
                    closed_commemt = temp['body'].encode("utf-8")
            if len(comments) > MaxCommentNum:
                MaxCommentNum = len(comments)
        CREATED_DATE = item['created_at']
        UPDATED_DATE = item['updated_at']
        CLOSED_DATE = item['closed_at']
        label_name = []
        for label in item['labels']:
            label_name.append(label['name'])
        labels_name = ",".join(label_name)
        it.append(title)
        it.append(labels_name)
        it.append(CREATED_DATE)
        it.append(UPDATED_DATE)
        it.append(CLOSED_DATE)
        it.append(body)
        it.append(closed_user)
        it.append(closed_commemt)
        for i in comments:
            it.append(i['body'].encode("utf-8"))
            it.append(i['author_association'])
        try:
            if len(it) != 0:
                save(it)
        except:
            print "This item contains an error character:"
            print it
            # print it
        # time.sleep(TIMEOUT)
    # exit()
