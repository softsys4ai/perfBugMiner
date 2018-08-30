import urllib2
import gzip
from StringIO import StringIO
import re
import time
headers = {
	'Host': 'github.com',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
	'Accept-Encoding': 'gzip, deflate, br',
	'Referer': 'https://github.com/',
	# 'Cookie': 'logged_in=yes; _ga=GA1.2.1149243158.1528184338; _octo=GH1.1.2070309403.1528184338; user_session=kJV4eJp0GvWHeHe5tCVA57aXxKyXHvEX5_-kevkVHaZoVF1H; dotcom_user=mrright2019; _gh_sess=V0hlQnUxSXR2bUZUcXNRNmlldldId0RRb0xPTk9lS2dVUmowRDlua1VLK1I1Ni8xUHFSWUtNMUh5U2svLzRQaURnWWNROWs1d1FTUCtEVWpWOSsyOGxCUnFLdUN2NlI4b1RnMFdpb2tZZUUvSWhzcGUyMEloSFU2Q2dPVTZ1eUEtLWRLbERkVWlSemxIZkorSmpvNTM0ZGc9PQ%3D%3D--39802c4d9dae171475ea38babe338588ff35a8c6; _gat=1; tz=Asia%2FShanghai',
	'Connection': 'keep-alive',
	'Upgrade-Insecure-Requests': 1,
	'Cache-Control': 'max-age=0'
	}

def GetHtmlFromAPI(url):
	try:
		request = urllib2.Request(url,headers = headers)
		try:
			response = urllib2.urlopen(request)
		except:
			return None
		JsonData = response.read()
		response.close()
		if len(JsonData) < 200:
			return None
		if response.info().get('Content-Encoding') == 'gzip':
			buf = StringIO(JsonData)
	    	f = gzip.GzipFile(fileobj=buf)
	    	JsonData = f.read()
		return JsonData
	except urllib2.URLError, e:
		print "Error Url:",url
		print e.reason
		return None


def parsecn(url):
	if url=="https://github.com/apps/stale":
		return 0
	html = GetHtmlFromAPI(url)
	if html==None:
		return 0
	key = re.findall(r'<h2 class=\"f4 text-normal mb-2\">\n.*?in the last year',html,re.S)
	if len(key)==0:
		return 0
	key = key[0].replace("in the last year","")
	return int(key.split(" ")[9].replace(",",""))


if __name__ == "__main__":
	a = 'https://github.com/fehiepsi'
	b = "https://github.com/Mrright2019"
	html = GetHtmlFromAPI(b)
	key = re.findall(r'<h2 class=\"f4 text-normal mb-2\">\n.*?in the last year',html,re.S)
	key = key[0].replace("in the last year","")
	print key.split(" ")[9]
	print key
