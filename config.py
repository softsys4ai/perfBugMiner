import urllib2
import gzip
from StringIO import StringIO
import json
client_id = 'bddd8203d9b4228a6b1d'

token = 'bad2ce6af1ad05ae5b100b7a2a19573c2ff90d01'

OpenFile = "Open Performance Issue for Tensorflow.csv"

ClosedFile = "closed Performance Issue for Tensorflow.csv"

repositorie = 'tensorflow'

owner = 'tensorflow'

TIMEOUT = 1

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


def GetJsonFromAPI(url):
	request = urllib2.Request(url,headers = headers)
	response = urllib2.urlopen(request)
	JsonData = response.read()
	if len(JsonData) < 200:
		return None
	response.close()
	if response.info().get('Content-Encoding') == 'gzip':
		buf = StringIO(JsonData)
    	f = gzip.GzipFile(fileobj=buf)
    	JsonData = f.read()
	return JsonData

urlend='client_id='+client_id+'&client_secret='+token
baseurl = 'https://api.github.com/repos/tensorflow/tensorflow/issues'#?page=50&state=closed'

timeline_url = 'https://api.github.com/repos/tensorflow/tensorflow/issues/'
if __name__ == "__main__":
	a = 'https://api.github.com/repos/tensorflow/tensorflow/issues/17787/timeline?'+urlend
	print GetJsonFromAPI(a)
# print GetJsonFromAPI(baseurl)
# print len(GetJsonFromAPI(baseurl))
