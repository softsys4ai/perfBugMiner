# -*- coding: utf-8 -*-
from config import *
import json
import csv
import time

csvFile = open(OpenFile,'wb+')
writer = csv.writer(csvFile)
titles = []
def save(it):
    csvfile = open(OpenFile, 'ab')
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
        comments.append(item)
    return comments

def SaveHeader():
    csvFile = open(OpenFile,'wb+')
    writer = csv.writer(csvFile)
    h=[]
    h.append("ID")
    h.append("GITHUB ID")
    h.append("ISSUE TITLE")
    h.append("ISSUE`S LABEL")
    h.append("ISSUE`S CREATED TIME")
    h.append("ISSUE`S UPDATED TIME")
    h.append("assignee")
    h.append("milestone")
    for i in range(1,40):
        h.append(str(i)+"th COMMENT")
        h.append(str(i)+"th COMMENT`S USER CHARACTER")
    writer.writerow(h)
    csvFile.close()

SaveHeader()

page = 1

MaxCommentNum = 0

id_ = 1

while True:
    url = baseurl + "?page="+str(page)+"&state=open"+"&"+urlend
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
        title = item['title'].encode("utf-8")
        body = item['body'].encode("utf-8")
        labels = json.dumps(item['labels']).encode("utf-8")
        Issue_Author_association = item['author_association']
        if "type:bug/performance" not in labels.lower() and  keyword not in title.lower() and keyword not in body.lower():
            continue
        if title in titles:
            continue
        titles.append(title)
        if item['comments'] is not 0:
            comments = getComments(comments_url+"?"+urlend)
            if len(comments) > MaxCommentNum:
                MaxCommentNum = len(comments)
        CREATED_DATE = item['created_at']
        UPDATED_DATE = item['updated_at']
        label_name = []
        for label in item['labels']:
            label_name.append(label['name'])
        labels_name = ",".join(label_name)
        it.append(str(id_))
        id_ += 1
        it.append(item['number'])
        it.append(title)
        it.append(labels_name)
        it.append(CREATED_DATE)
        it.append(UPDATED_DATE)
        if item["assignee"]:
            it.append(item["assignee"]["login"])
        else:
            it.append("")
        it.append(item['milestone'])
        it.append(body)
        it.append(Issue_Author_association)
        for i in comments:
            it.append(i['body'].encode("utf-8"))
            it.append(i['author_association'])
        try:
            if len(it) != 0:
                save(it)
        except:
            print "Storage error, error data is:"
            print it
        # time.sleep(TIMEOUT)
