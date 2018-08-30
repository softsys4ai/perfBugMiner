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
from Network import *
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

keywordslist = []

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
		if d[i]>40:
			keywordslist.append(i)
	return m





def getX(teams):
	# if dict_keyword is []:
	# dict_keyword = get_feature_word(all_word)
	# print len(dict_keyword)
	# print type(dict_keyword[0])
	X=[]
	for team in teams:
		x=[0]*len(dict_keyword)
		# print team
		armm = [0]*len(keywordslist)
		for i in team:
			if i in dict_keyword:
				x[dict_keyword.index(i)]=1
			if i in keywordslist:
				armm[keywordslist.index(i)]=1
		# print x
		X.append(x)
		armingmaxtrix.append(armm)
		# exit()
	X=np.array(X)
	# print X.shape
	return X



def word2x(word):
	x = [0]*len(dict_keyword)
	for w in word:
		if w in dict_keyword:
			x[dict_keyword.index(w)]=1
	x = np.array(x)
	return x


def word2arm(word):
	x = [0]*len(keywordslist)
	for w in word:
		if w in keywordslist:
			x[keywordslist.index(w)] = 1
	# x = np.array(x)
	return x


def getmode(X,Y):
	clf = GaussianNB().fit(X,Y.ravel())
	return clf

# dict_keyword = get_feature_word(all_word)
keywordslist += kwords
armingmaxtrix = []


modelabels = []
for l in label:
	if l in modelabels:
		continue
	modelabels.append(l)

Y = []
for l in label:
	y =[0]*len(modelabels)
	y[modelabels.index(l)] = 1
	Y.append(y)
Y = np.array(Y)
# print Y.shape


teams = traindata
teams = [setFeature(i) for i in teams]

dict_keyword = get_feature_word(all_word)

train_x = getX(teams)

# print train_x.shape
# print Y
# print Y.shape
  
mode = Network([train_x.shape[1],40,30,Y.shape[1]])
# a.put()
mode.fit(train_x,Y)
# res = mode.predict(train_x[10])
# print res.tolist().index(max(res.tolist()))
# print Y[10].tolist().index(max(Y[10].tolist()))
# print armingmaxtrix
# print keywordslist
# print len(keywordslist)
# print len(armingmaxtrix)
# print len(armingmaxtrix[0])

chapter_num = len(armingmaxtrix)
wordmatrix = [[0 for _ in keywordslist] for _ in keywordslist]
# print len(wordmatrix)
# print len(wordmatrix[0])

for _rowindex in range(0,chapter_num):
	for _firstindex in range(0,chapter_num):
		for _secondindex in range(_firstindex,chapter_num):
			if armingmaxtrix[_rowindex][_firstindex] is 0:
				continue
			if armingmaxtrix[_rowindex][_secondindex]:
				wordmatrix[_firstindex][_secondindex] += 1
				wordmatrix[_secondindex][_firstindex] += 1

# print max(armingmaxtrix)






# mode = getmode(train_X,Y)




# if __name__ == "__main__":
# 	mode = getmode()
 # 	# print acc(mode,test_X,test_Y)
