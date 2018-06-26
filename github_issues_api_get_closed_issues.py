# -*- coding: utf-8 -*-
from config import *
import json
import csv
import time
from plotdata import *

titles = []
ClosedLabel = {}
ClosedDateTime = {}


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
        item['body'] = comment['body']  # .replace("\n",'')
        item['author_association'] = comment['author_association']
        item['created_at'] = comment['created_at']
        item['updated_at'] = comment['updated_at']
        comments.append(item)
    return comments


def SaveHeader():
    csvFile = open(ClosedFile, 'wb')
    writer = csv.writer(csvFile)
    h = []
    h.append("ID")
    h.append("GITHUB ID")
    h.append("ISSUE TITLE")
    h.append("ISSUE`S LABEL")
    h.append("ISSUE`S CREATED TIME")
    h.append("ISSUE`S UPDATED TIME")
    h.append("ISSUE`S CLOSED TIME")
    h.append("assignee")
    h.append("milestone")
    h.append("ISSUE DESCRIPTION")
    h.append("CHARACTER OF THE USER WHO CREATED THE ISSUE")
    h.append("CHARACTER OF THE USER WHO CLOSED THE ISSUE")
    h.append("COMMENT OF THE USER WHO CLOSED THE ISSUE")
    for i in range(1, 40):
        h.append(str(i) + "th COMMENT")
        h.append(str(i) + "th COMMENT`S USER CHARACTER")
    writer.writerow(h)
    csvFile.close()


SaveHeader()


def DoClosed():
    page = 1
    id_ = 1
    MaxCommentNum = 0
    while True:
        url = baseurl + "?page=" + str(page) + "&state=closed" + "&" + urlend
        page += 1
        print u"Extracting:", url
        content = GetJsonFromAPI(url)
        if content is None:
            break
        js = json.loads(content)
        for item in js:
            it = []
            comments_url = item['comments_url']
            comments = []
            closed_user = item['author_association']
            closed_commemt = ''
            closed_at = item['closed_at']
            title = item['title'].encode("utf-8")
            labels = json.dumps(item['labels'])
            labels = labels.encode("utf-8")
            if item['body'] is None or len(item['body']) == 0:
                body = ""
            else:
                body = item['body'].encode('utf-8')
            label_name = []
            for label in item['labels']:
                label_name.append(label['name'])
            labels_name = ",".join(label_name)
            if ClosedLabel.has_key(item['closed_at'][:10]):
                ClosedLabel[item['closed_at'][:10]] = ClosedLabel[item['closed_at'][:10]] + label_name
            else:
                ClosedLabel[item['closed_at'][:10]] = label_name

            if ClosedDateTime.has_key(item['closed_at'][:10]):
                ClosedDateTime[item["closed_at"][:10]] = ClosedDateTime[item['closed_at'][:10]] + 1
            else:
                ClosedDateTime.setdefault(item['closed_at'][:10], 1)
            if "type:bug/performance" not in labels.lower() and keyword not in title.lower() and keyword not in body.lower():
                continue
            if title in titles:
                continue
            titles.append(title)
            time.sleep(TIMEOUT)
            if item['comments'] is not 0:
                comments = getComments(comments_url + "?" + urlend)
                for temp in comments:
                    if temp['created_at'] == closed_at or temp['updated_at'] == closed_at:
                        closed_user = temp['author_association']
                        closed_commemt = temp['body'].encode("utf-8")
                if len(comments) > MaxCommentNum:
                    MaxCommentNum = len(comments)
            CREATED_TIME = item['created_at']
            UPDATED_TIME = item['updated_at']
            CLOSED_TIME = item['closed_at']

            it.append(str(id_))
            id_ += 1
            it.append(item["number"])
            it.append(title)
            it.append(labels_name)
            it.append(CREATED_TIME)
            it.append(UPDATED_TIME)
            it.append(CLOSED_TIME)
            if item["assignee"]:
                it.append(item["assignee"]["login"])
            else:
                it.append("")
            it.append(item['milestone'])
            it.append(body)
            it.append(item['author_association'])
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


DoClosed()

ClosedDateTimeKeys = sorted(ClosedDateTime.keys(), date_compare)

SaveWeek(ClosedDateTimeKeys, ClosedDateTime, DirPath=ClosedWeekDir, ylabel="Closed Issue Num")
SaveMonth(ClosedDateTimeKeys, ClosedDateTime, DirPath=ClosedMonthDir, ylabel="Closed Issue Num")
SaveYear(ClosedDateTimeKeys, ClosedDateTime, DirPath=ClosedYearDir, ylabel="Closed Issue Num")

PlotChart1(ClosedDateTimeKeys, ClosedDateTime, filename=CHART2, title="issue closed number weekly")

PlotMonthPie(ClosedLabel, ClosedDateTimeKeys, DirPath=ClosedMonthLabelDir)
PlotYearPie(ClosedLabel, ClosedDateTimeKeys, DirPath=ClosedYearLabelDir, fsize=(30, 30))
