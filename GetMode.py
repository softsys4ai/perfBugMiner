#coding:utf-8
import nltk
import math
import jieba
import numpy as np
import string
import csv
import random
from sklearn import svm 
from nltk.corpus import stopwords
from collections import Counter
from nltk.stem.porter import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeRegressor  
from sklearn.ensemble import RandomForestRegressor  
from sklearn.naive_bayes import GaussianNB 
from config import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')
all_word=[]
dict_keyword=[]

test_list1 = []

traindata = []
trainx = []
tariny = []
label = []


with open("traindata") as f:
    reader = csv.reader(f)
    for row in reader:
    	traindata.append(row[0].lower())
    	label.append(row[1])





def setFeature(words):
	global all_word
	words = words.replace("*","")
	words = words.replace(")","")
	words = words.replace("=","")
	words = words.replace("-","")
	words = words.replace("+","")
	words = words.replace("/","")
	words = words.replace("{","")
	words = words.replace("}","")
	words = words.replace("'","")
	words = words.replace("@","")
	words = words.replace(","," ")
	words = words.replace("."," ")
	words = words.replace("?"," ")
	words = words.replace("`","")
	words = words.replace(":"," ")
	words = words.replace("(","")
	words = words.replace("#","")
	cut_words = nltk.word_tokenize(words)
	res = [w for w in cut_words if w not in stopwords.words('english')]
	all_word = all_word + res
	# print 'parse one'
	# exit()
	return res

def get_feature_word(teams):
	d={}
	m=[]
	for i in teams:
		if d.has_key(i):
			d[i] = d[i]+1
		else:
			d.setdefault(i,1)
	for i in d:
		if d[i]>=200:# and d[i]<=3000:
			m.append(i)
	return m

def getX(teams):
	dict_keyword = get_feature_word(all_word)
	global kwords
	kwords = kwords+dict_keyword
	# print len(dict_keyword)
	# print type(dict_keyword[0])
	X=[]
	for team in teams:
		x=[0]*len(dict_keyword)
		# print team
		for i in team:
			if i in dict_keyword:
				x[dict_keyword.index(i)]=1
		# print x
		X.append(x)
		# exit()
	X=np.array(X)
	# print X.shape
	return X




def getmode(X,Y):
	# clf = RandomForestRegressor()
	# clf.fit(X,Y.ravel())
	#svm
	# clf = svm.SVC()
	# clf.fit(X,Y.ravel())
	clf = GaussianNB().fit(X,Y.ravel())
	return clf

modelabels = []
for l in label:
	if l in modelabels:
		continue
	modelabels.append(l)

Y = []
for l in label:
	Y.append(modelabels.index(l))
Y = np.array(Y)
# print Y.shape

teams = traindata
teams = [setFeature(i) for i in teams]


# test_list = [setFeature(i) for i in test_list1]
train_X = getX(teams)

# print train_X.shape
mode = getmode(train_X,Y)


def acc(mode,test_X,test_Y):
	_Y = mode.predict(test_X)
	_Y = np.array([_Y])
	_y = np.transpose(_Y)
	res = (test_Y==_y)
	return float(np.sum(res==True))/20000.0



# if __name__ == "__main__":
# 	mode = getmode()
# 	# print acc(mode,test_X,test_Y)



# predict_y = mode.predict_y
