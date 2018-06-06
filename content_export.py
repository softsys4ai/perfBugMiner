# -*- coding: utf-8 -*-
from config import *
import json
import csv
import time

csvFile = open(OpenFile,'wb+')
writer = csv.writer(csvFile)
def save(it):
    # csvfile = open(OpenFile, 'a')
    # writer = csv.writer(csvfile)
    writer.writerow(it)
    # csvfile.close()

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
    h=[]
    h.append("ISSUE TITLE")
    h.append("ISSUE`S LABEL")
    h.append("ISSUE`S TIMELINE")
    for i in range(1,40):
        h.append(str(i)+"th COMMENT")
        h.append(str(i)+"th COMMENT`S USER CHARACTER")
    writer.writerow(h)
    # csvFile.close()

SaveHeader()

page = 1

MaxCommentNum = 0

while True:
    url = baseurl + "?page="+str(page)+"&state=open"+"&"+urlend
    page +=1
    print "EXTRACTING:",url
    content = GetJsonFromAPI(url)
    if content is None:
        break
    js = json.loads(content)
    for item in js:
        it = []
        comments_url = item['comments_url']
        time.sleep(TIMEOUT)
        comments = []
        if item['comments'] is not 0:
            comments = getComments(comments_url+"?"+urlend)
            if len(comments) > MaxCommentNum:
                MaxCommentNum = len(comments)
        title = item['title'].encode("utf-8")
        labels = json.dumps(item['labels']).encode("utf-8")
        timeline = "create_at:"+item['created_at']+",updated_at:"+item['updated_at']+",author_association:"+item['author_association']
        it.append(title)
        it.append(labels)
        it.append(timeline)
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
