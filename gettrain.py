#coding:utf-8
# -*- coding: utf-8 -*-
from config import *
import json
import csv
import time
from plotdata import *
import os
from ParseConNum import *
import pickle
from GetKeyword import *

def existData(ResFile=ResFile):
    return os.path.exists(ResFile)

def GetLast(ResFile=ResFile):
    f = open(ResFile,'r')
    data = pickle.load(f)
    f.close()
    return data

def SaveData(data,ResFile=ResFile):
    f = open(ResFile,'w')
    pickle.dump(data,f)
    f.close()

def save(it):
    csvfile = open(OpenFile, 'ab')
    writer = csv.writer(csvfile)
    writer.writerow(it)
    csvfile.close()


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
    h.append("ISSUE DESCIPTION")
    h.append("CHARACTER OF THE USER WHO CREATED THE ISSUE")
    for i in range(2,40):
        h.append(str(i)+"th COMMENT")
        h.append(str(i)+"th COMMENT`S USER CHARACTER")
    writer.writerow(h)
    csvFile.close()





def getComments(url):
    content = GetJsonFromAPI(url)
    if content is None:
        return []
    js = json.loads(content)
    comments = []
    mn = 0.0
    an = 0.0
    temp = 0.0
    uid = []
    for comment in js:
        item = {}
        item['body'] = comment['body']#.replace("\n",'')MEMBER
        item['author_association'] = comment['author_association']
        print comment['user']['html_url']
        # cnum = parsecn(comment['user']['html_url'])
        # time.sleep(TIMEOUT)
        comments.append(item)
    return comments


def ParseText(label):
    label = label.replace(" ","")
    label = label.replace("\r","")
    label = label.replace("\n","")
    label = label.replace("\t","")
    return label

def savedata(data,label):
    with open('traindata','a+') as f:
        writer = csv.writer(f)
        writer.writerow([data,label])



csv_file = csv.reader(open('data.csv','r'))
for c in csv_file:
    url = 'https://api.github.com/repos/tensorflow/tensorflow/issues/'+c[0].split("/")[-1]+"?"+urlend
    print url
    label = ParseText(c[1].lower())
    if not label:
        continue
    item = GetJsonFromAPI(url)
    if item is None:
        continue
    item = json.loads(item)
    body = item['body']
    comments = item['comments']
    commenturl = item['comments_url']
    comment_list = []
    if comments is not 0:
        comment_list = getComments(commenturl+"?"+urlend)
    for c in comment_list:
        body += "\n"+c['body']
    body = body.replace("\n","")
    body = body.replace("\r","")
    body = body.replace("\t","")
    # body = ParseText(body)
    # print body
    print type(body)
    body = body.encode('utf-8')
    try:
        savedata(body,label)
    except:
        print body

