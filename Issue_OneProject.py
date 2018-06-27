# -*- coding: utf-8 -*-
from config import *
import json
import csv
import time
from plotdata import *
import os
from ParseConNum import *
import pickle

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

AllData = {}
if existData(ResFile) is not True:
    AllData['page'] = 1
    AllData['proname'] = proname
    AllData['MemberComCharNumRate'] = []
    AllData['MemberCommentRate'] = []
    AllData['ProUserConNum'] = []
    AllData['TheUserCon'] = []
    AllData['LabelDateItems'] = {}
    AllData['LabelComNum'] = {}
    AllData['OpenDateLabel'] = {}
    AllData['OpenDateNum'] = {}
    AllData['UserCon'] = {}
    AllData['ProIssueDays'] = []
    AllData['ProComNum'] = []
    AllData['id_'] = 1
    AllData["User"] = {}
    AllData["ComPage"] = 1
    AllData['UserCommit'] = {}
    # AllData['MemberCommitNum'] = []
    # AllData['NotMemberCommitNum'] = []
    # SaveData(AllData,ResFile)
    SaveHeader()
else:
    AllData = GetLast(ResFile=ResFile)
    # AllData['page'] = AllData['page']+1



#chart7
UserCon = {}
#end chart7

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
        if AllData['User'].has_key(comment['user']['id']):
            pass
        else:
            AllData['User'][comment['user']['id']] = comment['author_association']
        if comment['user']['id'] in AllData['TheUserCon']:
            pass
        else:
            if AllData['UserCon'].has_key(comment['user']['id']):
                AllData['TheUserCon'].append(comment['user']['id'])
                pass
            else:
                print comment['user']['html_url']
                cnum = parsecn(comment['user']['html_url'])
                time.sleep(TIMEOUT)
                if cnum <10000:
                    AllData['UserCon'][comment['user']['id']] = cnum
                    AllData['TheUserCon'].append(comment['user']['id'])
        if comment['user']['id'] in uid:
            pass
        else:
            if comment['author_association'] == 'MEMBER':
                temp += 1
            uid.append(comment['user']['id'])
        if comment['author_association'] == 'MEMBER':
            mn+=1
        an+=1
        comments.append(item)
    AllData['MemberComCharNumRate'].append(temp/len(uid))
    AllData['MemberCommentRate'].append(mn/an)
    return comments


while True:
    url = baseurl + "?page="+str(AllData['page'])+"&state="+"&"+urlend
    # if AllData['page']>=2:
    #     break
    if AllData['page'] % 5 ==0:
        print u"Saving Data"
        SaveData(AllData,ResFile)
    AllData['page'] += 1
    print u"Extracting:",url
    content = GetJsonFromAPI(url)
    if content is None:
        SaveData(AllData,ResFile)
        break
    js = json.loads(content)
    for item in js:
        it = []
        if AllData['User'].has_key(item['user']['id']):
            pass
        else:
            AllData['User'][item['user']['id']] = item['author_association']
        comment_url = item['comments_url']
        comments = []
        title = item['title'].encode("utf-8")
        if item['body']==None or item['body'] == "":
            body = ""
        else:
            body = item['body'].encode("utf-8")
        if item['comments'] is not 0:
            comments = getComments(comment_url+"?"+urlend)
        label_name = []
        if item['state'] == 'open':
            tc = Caltime(item['created_at'][:10],today)
        else:
            tc = Caltime(item['created_at'][:10],item['closed_at'][:10])
        AllData['ProIssueDays'].append(tc)
        if item['comments']<700:
            AllData['ProComNum'].append(item['comments'])
        for label in item['labels']:
            label_name.append(label['name'])
            if label['name']!=None:
                if AllData['LabelDateItems'].has_key(label['name']):
                    AllData['LabelDateItems'][label['name']].append(tc)
                else:
                    AllData['LabelDateItems'][label['name']] = [tc]
                if item['comments']>700:
                    continue
                if AllData['LabelComNum'].has_key(label['name']):
                    AllData['LabelComNum'][label['name']].append(item['comments'])
                else:
                    AllData['LabelComNum'][label['name']] = [item['comments']]
        labels_name = ",".join(label_name)
        if AllData['OpenDateLabel'].has_key(item['created_at'][:10]):
            AllData['OpenDateLabel'][item['created_at'][:10]] = AllData['OpenDateLabel'][item['created_at'][:10]] + label_name
        else:
            AllData['OpenDateLabel'][item['created_at'][:10]] = label_name
        if AllData['OpenDateNum'].has_key(item['created_at'][:10]):
            AllData['OpenDateNum'][item['created_at'][:10]] = AllData['OpenDateNum'][item['created_at'][:10]] +1
        else:
            AllData['OpenDateNum'][item['created_at'][:10]] = 1
        labels = json.dumps(item['labels']).encode("utf-8")
        Issue_Author_association = item['author_association']
        if item['state'] != "open":
            continue
        if "type:bug/performance" not in labels.lower():
            continue
        CREATED_TIME = item['created_at']
        UPDATED_TIME = item['updated_at']
        it.append(str(AllData['id_']))
        AllData['id_'] += 1
        it.append(item['number'])
        it.append(title)
        it.append(labels_name)
        it.append(CREATED_TIME )
        it.append(UPDATED_TIME)
        if item['assignee']:
            it.append(item['assignee']['login'])
        else:
            it.append("")
        it.append(item['milestone'])
        it.append(body)
        it.append(Issue_Author_association)
        for i in comments:
            it.append(i['body'].encode("utf-8"))
            it.append(i['author_association'])
        try:
            if len(it) !=0:
                save(it)
        except:
            print u"Storage error, error data is:"
            print it
    #exit()

OpenDateTimeKeys = sorted(AllData['OpenDateNum'].keys(),date_compare)
SaveWeek(OpenDateTimeKeys,AllData['OpenDateNum'],DirPath=OpenWeekDir)

SaveMonth(OpenDateTimeKeys,AllData['OpenDateNum'],DirPath = OpenMonthDir)

SaveYear(OpenDateTimeKeys,AllData['OpenDateNum'],DirPath = OpenYearDir)

PlotMonthPie(AllData['OpenDateLabel'],OpenDateTimeKeys,DirPath = OpenMonthLabelDir)

PlotYearPie(AllData['OpenDateLabel'],OpenDateTimeKeys,DirPath = OpenYearLabelDir,fsize=(30,30))

PlotChart1(OpenDateTimeKeys,AllData['OpenDateNum'])

PlotChart3(AllData['LabelDateItems'],filename=CHART3)

PlotChart4(AllData['LabelComNum'],filename=CHART4)


while True:
    commitsurl = baseurl.replace("issues","commits")+"?page="+str(AllData["ComPage"])+"&"+urlend
    CommitData = GetJsonFromAPI(commitsurl)
    print u"Extracting",commitsurl
    # if AllData["ComPage"]>50:
    #     break
    if CommitData is None:
        SaveData(AllData,ResFile)
        break
    js = json.loads(CommitData)
    for commit in js:
        if commit is None:
            continue
        if commit['author']==None:
            continue
        if commit ['author'].has_key('id') is not True:
            continue
        if commit ['author'].has_key("login") and commit['author']['login'] in ProRobots:
            continue
        loginid = commit['author']['id']
        if loginid in AllData['UserCommit']:
            AllData['UserCommit'][loginid] += 1
        else:
            AllData['UserCommit'][loginid] = 1
    AllData["ComPage"] += 1
    if AllData["ComPage"]%20 ==0:
        print u"Saving Data"
        SaveData(AllData,ResFile)


Member = []
NotMember = []
PlotChartPCL = ["member","not member"]

for userid in AllData['UserCommit']:
    if AllData['User'].has_key(userid) and AllData['User'][userid].lower() == "member":
        Member.append(AllData['UserCommit'][userid])
    else:
        NotMember.append(AllData['UserCommit'][userid])

PlotChartPC = [Member,NotMember]

PlotProChart34(PlotChartPC,PlotChartPCL,xlabel="member or not",ylabel = "number of  commits",filename = "UserCommit.png")
