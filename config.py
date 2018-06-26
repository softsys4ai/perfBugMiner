#coding:utf-8
import urllib2
import gzip
from StringIO import StringIO
import json
import datetime
import time
import os


import ssl
ssl._create_default_https_context = ssl._create_unverified_context

OpenDir = "Open"
ClosedDir = "Closed"
LabelDir = "Label"
WeekDir = "Week"
MonthDir = "Month"
YearDir = "Year"


CHART1 = "chart1.jpg"
CHART2 = "chart2.jpg"
CHART3 = "chart3.jpg"
CHART4 = "chart4.jpg"
CHART5 = "chart5.jpg"
CHART6 = "chart6.jpg"
CHART7 = "chart7.jpg"

if not os.path.exists(OpenDir):
    os.makedirs(OpenDir)
if not os.path.exists(ClosedDir):
    os.makedirs(ClosedDir)

OpenLabelDir = OpenDir+"/"+LabelDir
if not os.path.exists(OpenLabelDir):
    os.makedirs(OpenLabelDir)
ClosedLabelDir = ClosedDir+"/"+LabelDir
if not os.path.exists(ClosedLabelDir):
    os.makedirs(ClosedLabelDir)

OpenMonthLabelDir = OpenLabelDir + "/" +MonthDir
if not os.path.exists(OpenMonthLabelDir):
    os.makedirs(OpenMonthLabelDir)

ClosedMonthLabelDir = ClosedLabelDir + "/" +MonthDir
if not os.path.exists(ClosedMonthLabelDir):
    os.makedirs(ClosedMonthLabelDir)

OpenYearLabelDir = OpenLabelDir + "/"+YearDir
if not os.path.exists(OpenYearLabelDir):
    os.makedirs(OpenYearLabelDir)

ClosedYearLabelDir = ClosedLabelDir + "/"+YearDir
if not os.path.exists(ClosedYearLabelDir):
    os.makedirs(ClosedYearLabelDir)

OpenWeekDir = OpenDir +"/"+WeekDir
if not os.path.exists(OpenWeekDir):
    os.makedirs(OpenWeekDir)
ClosedWeekDir = ClosedDir +"/"+WeekDir
if not os.path.exists(ClosedWeekDir):
    os.makedirs(ClosedWeekDir)

OpenMonthDir = OpenDir +"/"+MonthDir
if not os.path.exists(OpenMonthDir):
    os.makedirs(OpenMonthDir)
ClosedMonthDir = ClosedDir +"/"+MonthDir
if not os.path.exists(ClosedMonthDir):
    os.makedirs(ClosedMonthDir)


OpenYearDir = OpenDir +"/"+YearDir
if not os.path.exists(OpenYearDir):
    os.makedirs(OpenYearDir)
ClosedYearDir = ClosedDir +"/"+YearDir
if not os.path.exists(ClosedYearDir):
    os.makedirs(ClosedYearDir)


client_id = 'bddd8203d9b4228a6b1d'
token = 'bad2ce6af1ad05ae5b100b7a2a19573c2ff90d01'
OpenFile = "Open Performance Issue for Tensorflow.csv"
ClosedFile = "closed Performance Issue for Tensorflow.csv"
repositorie = 'tensorflow'
owner = 'tensorflow'
TIMEOUT = 0
keyword = "Performance"
headers = {
	'Host': 'api.github.com',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
	'Accept': 'application/vnd.github.mockingbird-preview',#text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
	'Accept-Encoding': 'gzip, deflate, br',
	'Cookie': 'logged_in=yes; _ga=GA1.2.1149243158.1528184338; _octo=GH1.1.2070309403.1528184338; _gid=GA1.2.53887231.1528184538; dotcom_user=mrright2019',
	'Connection': 'keep-alive',
	'Upgrade-Insecure-Requests': '1',
	'If-None-Match': 'W/"6c7c01a7a54f5cc9a2ec9fffc6b68a56"',
	'Cache-Control': 'max-age=0',
	'Authorization':token
	}



today = datetime.datetime.now().strftime("%Y-%m-%d")

def date_compare(item1, item2):
    t1 = time.mktime(time.strptime(item1, '%Y-%m-%d'))
    t2 = time.mktime(time.strptime(item2, '%Y-%m-%d'))
    # print(t1, t2)
    if t1 < t2:
        return -1
    elif t1 > t2:
        return 1
    else:
        return 0

def Caltime(date1,date2):
    date1=time.strptime(date1,"%Y-%m-%d")
    date2=time.strptime(date2,"%Y-%m-%d")
    date1=datetime.datetime(date1[0],date1[1],date1[2])
    date2=datetime.datetime(date2[0],date2[1],date2[2])
    if len(str(date2-date1).split(" "))==1:
    	return 0
    return int(str(date2-date1).split(" ")[0])

def GetDayAfterN(item1,n):
	y = int(item1[:4])
	m = int(item1[5:7])
	d = int(item1[8:])
	the_date = datetime.datetime(y,m,d)
	data = the_date+datetime.timedelta(days=n)
	time_format = data.strftime('%Y-%m-%d')
	return time_format


def GetJsonFromAPI(url):
	try:
		request = urllib2.Request(url,headers = headers)
		try:
			response = urllib2.urlopen(request)
		except:
			print "httplib Error,bad url:",url
			return None
		JsonData = response.read()
		if len(JsonData) < 200:
			return None
		response.close()
		if response.info().get('Content-Encoding') == 'gzip':
			buf = StringIO(JsonData)
	    	f = gzip.GzipFile(fileobj=buf)
	    	JsonData = f.read()
		return JsonData
	except urllib2.URLError, e:
		print "Error Url:",url
		print e.reason
		return None

urlend='client_id='+client_id+'&client_secret='+token
baseurl = 'https://api.github.com/repos/tensorflow/tensorflow/issues'#?page=50&state=closed'keras-team/keras

proname = "tensorflow"

ResFile = proname+".json"

ProRobots = []

# flags = [1,0,0,0]
# baseurls = [
# 'https://api.github.com/repos/pytorch/pytorch/issues',
# 'https://api.github.com/repos/keras-team/keras/issues',
# 'https://api.github.com/repos/opencv/opencv/issues',
# 'https://api.github.com/repos/tensorflow/tensorflow/issues'
# ]
# ProName=['pytorch','keras','opencv','tensorflow']

timeline_url = 'https://api.github.com/repos/tensorflow/tensorflow/issues/'

if __name__ == "__main__":
	a = 'https://github.com/fehiepsi'
	# print GetJsonFromAPI(a)
	print GetDayAfterN("2018-11-12",7)
	print Caltime("2018-06-13","2018-06-19")
	print today
	print Caltime(today,"2018-06-18")
