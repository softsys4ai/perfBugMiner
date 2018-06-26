# -*- coding: utf-8 -*-
from config import *
import json
import csv
import time
from plotdata import *
import os
from ParseConNum import *
import pickle

def GetProData(ResFile):
    f = open("PLOTPRO/"+ResFile,'r')
    data = pickle.load(f)
    f.close()
    return data

Files = os.listdir("PLOTPRO")

ProName = []

MemberCommentCharNumRate = []
MemberCommentRate = []
ProIssueDays = []
ProComNum = []
PLOT7 = []

ProCommit = []


for file in Files:
	data = GetProData(file)
	MemberCommentCharNumRate.append(data['MemberComCharNumRate'])
	MemberCommentRate.append(data['MemberCommentRate'])
	ProName.append(file[:-5])
	ProIssueDays.append(data['ProIssueDays'])
	ProComNum.append(data['ProComNum'])
	temp = []
	com = []
	for j in data['TheUserCon']:
		temp.append(data['UserCon'][j])
	for u in data['UserCommit']:
		com.append(data['UserCommit'][u])
	PLOT7.append(temp)
	ProCommit.append(com)

PlotChart5(MemberCommentCharNumRate,ProName,filename=CHART5)
PlotChart6(MemberCommentRate,ProName,filename=CHART6)
PlotChart7(PLOT7,ProName,filename=CHART7)

PlotProChart34(ProIssueDays,ProName,filename = "ProChart3")
PlotProChart34(ProComNum,ProName,ylabel="Issue Comments Number",filename = "ProChart4")
PlotProChart34(ProCommit,ProName,ylabel="number of commits",filename = "ProCommitNumber")
