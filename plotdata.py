# coding:utf-8
import matplotlib.pyplot as plt
from config import *


# plt.ion()


def PlotXX(num, labels, fsize=(30, 10), xlabel="", ylabel="", filename=CHART3, rotation=30):
    plt.figure(figsize=fsize)
    plt.boxplot(num, labels=labels)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=rotation)
    plt.savefig(filename)
    plt.close()


def PlotJX(x1, y1, title="", fsize=(12, 10), xlabel="", ylabel="", label="", filename=None, rotation=60):
    plt.figure(figsize=fsize)
    plt.title(title)
    plt.plot(x1, y1, label=label, linewidth=2, color='r', marker='o',
             markerfacecolor='blue', markersize=5)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=rotation)
    for a, b in zip(x1, y1):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=12)
        # plt.legend()
    # plt.show()
    if filename:
        plt.savefig(filename)
    plt.close()


def SaveWeek(keys, DateTime, DirPath=OpenWeekDir, xlabel="date", ylabel="Issue Created Num", rotation=360):
    if keys is None:
        return
    FirstDay = keys[0]
    EndDay = GetDayAfterN(FirstDay, 6)
    DeltaX = []
    DeltaY = []
    deltaNum = 1
    while True:
        if date_compare(FirstDay, keys[-1]) == 1:
            break
        for i in range(0, 7):
            day = GetDayAfterN(FirstDay, i)
            DeltaX.append(day)
            if DateTime.has_key(day):
                DeltaY.append(DateTime[day])
            else:
                DeltaY.append(0)
        PlotJX(DeltaX, DeltaY, title=str(deltaNum) + "st Week", xlabel=xlabel, ylabel=ylabel,
               filename=DirPath + "/" + str(deltaNum) + "st.png", rotation=rotation)
        FirstDay = GetDayAfterN(FirstDay, 7)
        EndDay = GetDayAfterN(FirstDay, 6)
        DeltaX = []
        DeltaY = []
        deltaNum += 1


def SaveMonth(keys, DateTime, DirPath=OpenMonthDir, xlabel="date", ylabel="Issue Created Num", rotation=30):
    if keys is None:
        return
    FirstDay = keys[0]
    EndDay = GetDayAfterN(FirstDay, 27)
    DeltaX = []
    DeltaY = []
    deltaNum = 1
    while True:
        if date_compare(FirstDay, keys[-1]) == 1:
            break
        for p in range(0, 4):
            temp = 0
            DeltaX.append(GetDayAfterN(FirstDay, p * 7) + "-" + GetDayAfterN(FirstDay, (p + 1) * 7))
            for i in range(0, 7):
                day = GetDayAfterN(FirstDay, p * 7 + i)
                if DateTime.has_key(day):
                    temp += DateTime[day]
            DeltaY.append(temp)
        PlotJX(DeltaX, DeltaY, title=str(deltaNum) + "st Month", xlabel=xlabel, ylabel=ylabel,
               filename=DirPath + "/" + str(deltaNum) + "st.png", rotation=rotation)
        FirstDay = GetDayAfterN(FirstDay, 28)
        EndDay = GetDayAfterN(FirstDay, 27)
        DeltaX = []
        DeltaY = []
        deltaNum += 1


def SaveYear(keys, DateTime, DirPath=OpenYearDir, xlabel="date", ylabel="Issue Created Num", rotation=30):
    if keys is None:
        return
    FirstDay = keys[0]
    EndDay = GetDayAfterN(FirstDay, 365)
    DeltaX = []
    DeltaY = []
    deltaNum = 1
    while True:
        if date_compare(FirstDay, keys[-1]) == 1:
            break
        for p in range(0, 12):
            temp = 0
            DeltaX.append(GetDayAfterN(FirstDay, p * 30) + "-" + GetDayAfterN(FirstDay, (p + 1) * 30))
            for i in range(0, 30):
                day = GetDayAfterN(FirstDay, p * 30 + i)
                if DateTime.has_key(day):
                    temp += DateTime[day]
            DeltaY.append(temp)
        PlotJX(DeltaX, DeltaY, title=str(deltaNum) + "st Year", xlabel=xlabel, ylabel=ylabel,
               filename=DirPath + "/" + str(deltaNum) + "st.png", rotation=rotation)
        FirstDay = GetDayAfterN(FirstDay, 366)
        EndDay = GetDayAfterN(FirstDay, 365)
        DeltaX = []
        DeltaY = []
        deltaNum += 1


'''
def SaveWeekImg(x,y,n=6,Dirname=OpenWeekDir ,title="Week",fsize=(12,10),xlabel="Date" ,ylabel="Issue Created Num"):
    if x is None:
        return
    FirstDay = x[0]
    FirstDay_WeekEnd = GetDayAfterN(FirstDay,n)
    WeekX=[]
    WeekY=[]
    deltaNum = 1
    for day,num in zip(x,y):
        if date_compare(FirstDay_WeekEnd,day)==-1:
            FirstDay = day
            FirstDay_WeekEnd = GetDayAfterN(FirstDay,n)
            PlotJX(WeekX,WeekY,fsize=fsize,title=str(deltaNum)+"st "+title,xlabel=xlabel,ylabel=ylabel,filename=Dirname+"/"+str(deltaNum)+"st.png",rotation=360)
            deltaNum += 1
            WeekX = []
            WeekY = []
        WeekX.append(day)
        WeekY.append(num)
    PlotJX(WeekX,WeekY,fsize=fsize,title=str(deltaNum)+"st "+title,xlabel=xlabel,ylabel=ylabel,filename=Dirname+"/"+str(deltaNum)+"st.png",rotation=360)


def SaveMonthImg(x,y,DirPath = OpenMonthDir,xlabel="date",ylabel = "Issue Created Num",rotation=30):
    if x is None:
        return
    FirstDay = x[0]
    FirstDay_WeekEnd = GetDayAfterN(FirstDay,6)
    DeltaX=[]
    DeltaY=[]
    MonthNum = 1
    deltaN = 0
    for day,num in zip(x,y):
        if date_compare(FirstDay_WeekEnd,day)==-1:
            DeltaX.append(FirstDay+"-"+FirstDay_WeekEnd)
            DeltaY.append(deltaN)
            FirstDay = GetDayAfterN(FirstDay,7)
            FirstDay_WeekEnd = GetDayAfterN(FirstDay,6)
            deltaN = 0
        if len(DeltaX) ==4:
            PlotJX(DeltaX,DeltaY,title=str(MonthNum)+"st Month",xlabel =xlabel,ylabel=ylabel,filename = DirPath+"/"+str(MonthNum)+"st.png",rotation=rotation)
            DeltaX = []
            DeltaY = []
            MonthNum +=1
        deltaN = deltaN+num
    if len(DeltaX) == 0:
        return
    PlotJX(DeltaX,DeltaY,title=str(MonthNum)+"st Month",xlabel = xlabel,ylabel=ylabel,filename = DirPath+"/"+str(MonthNum)+"st.png",rotation=rotation)


def SaveYearImg(x,y,DirPath=OpenYearDir,xlabel="date",ylabel="Issue Created Num",rotation=30):
    if x is None:
        return
    FirstDay = x[0]
    FirstDay_MonthEnd = GetDayAfterN(FirstDay,30)
    DeltaX=[]
    DeltaY=[]
    MonthNum = 1
    deltaN = 0
    for day,num in zip(x,y):
        if date_compare(FirstDay_MonthEnd,day)==-1:
            DeltaX.append(FirstDay+"-"+FirstDay_MonthEnd)
            DeltaY.append(deltaN)
            FirstDay = GetDayAfterN(FirstDay,31)
            FirstDay_MonthEnd = GetDayAfterN(FirstDay,30)
            deltaN = 0
        if len(DeltaX) ==12:
            PlotJX(DeltaX,DeltaY,title=str(MonthNum)+"st Year",xlabel = xlabel,ylabel=ylabel,filename = DirPath+"/"+str(MonthNum)+"st.png",rotation=rotation)
            # print DeltaX,DeltaY
            DeltaX = []
            DeltaY = []
            MonthNum +=1
        deltaN = deltaN+num
    if len(DeltaX) == 0:
        return
    PlotJX(DeltaX,DeltaY,title=str(MonthNum)+"st Year",xlabel = xlabel,ylabel=ylabel,filename = DirPath+"/"+str(MonthNum)+"st.png",rotation=rotation)
'''


def PlotMonthPie(datelabel, keys, DirPath=OpenMonthLabelDir):
    if len(keys) == 0:
        return
    FirstDay = keys[0]
    EndDay = GetDayAfterN(FirstDay, 29)
    DateList = [GetDayAfterN(FirstDay, i) for i in range(0, 30)]
    LabelX = []
    LabelY = []
    MonthNum = 1
    while True:
        if date_compare(FirstDay, keys[-1]) == 1:
            break
        for day in DateList:
            if datelabel.has_key(day):
                labels = datelabel[day]
                for label in labels:
                    if label in LabelX:
                        Lindex = LabelX.index(label)
                        LabelY[Lindex] = LabelY[Lindex] + 1
                    else:
                        LabelX.append(label)
                        LabelY.append(1)
        PlotPie(LabelX, LabelY, title=FirstDay + "-" + EndDay,
                filename=DirPath + "/" + FirstDay + "-" + EndDay + ".jpg")
        LabelX = []
        LabelY = []
        FirstDay = GetDayAfterN(FirstDay, 30)
        EndDay = GetDayAfterN(FirstDay, 29)
        DateList = [GetDayAfterN(FirstDay, i) for i in range(0, 30)]
        MonthNum += 1


def PlotYearPie(datelabel, keys, fsize=(10, 10), DirPath=OpenYearLabelDir):
    if len(keys) == 0:
        return
    FirstDay = keys[0]
    EndDay = GetDayAfterN(FirstDay, 365)
    DateList = [GetDayAfterN(FirstDay, i) for i in range(0, 366)]
    LabelX = []
    LabelY = []
    MonthNum = 1
    while True:
        if date_compare(FirstDay, keys[-1]) == 1:
            break
        for day in DateList:
            if datelabel.has_key(day):
                labels = datelabel[day]
                for label in labels:
                    if label in LabelX:
                        Lindex = LabelX.index(label)
                        LabelY[Lindex] = LabelY[Lindex] + 1
                    else:
                        LabelX.append(label)
                        LabelY.append(1)
        PlotPie(LabelX, LabelY, fsize=fsize, title=FirstDay + "-" + EndDay,
                filename=DirPath + "/" + FirstDay + "-" + EndDay + ".jpg")
        LabelX = []
        LabelY = []
        FirstDay = GetDayAfterN(FirstDay, 366)
        EndDay = GetDayAfterN(FirstDay, 365)
        DateList = [GetDayAfterN(FirstDay, i) for i in range(0, 366)]
        MonthNum += 1


def PlotPie(x, y, fsize=(10, 10), title="pie chart", filename=None):
    plt.figure(figsize=fsize)
    plt.pie(y, labels=x, autopct="%1.2f%%")
    plt.title(title)
    # plt.show()
    if filename:
        plt.savefig(filename)
    plt.close()


def PlotChart1(keys, dic, filename=CHART1, title=u"Everyweek issue Created number", xlabel=u"Week", ylabel=u"Number",
               fsize=(80, 20), rotation=30):
    if len(keys) == 0:
        return
    X = []
    Y = []
    FirstDay = keys[0]
    WeekEnd = GetDayAfterN(FirstDay, 6)
    DateList = [GetDayAfterN(FirstDay, i) for i in range(0, 7)]
    while True:
        if date_compare(FirstDay, keys[-1]) == 1:
            break
        X.append(FirstDay + "-" + WeekEnd)
        wsum = 0
        for day in DateList:
            if dic.has_key(day):
                wsum = wsum + dic[day]
        Y.append(wsum)
        FirstDay = GetDayAfterN(FirstDay, 7)
        WeekEnd = GetDayAfterN(FirstDay, 6)
        DateList = [GetDayAfterN(FirstDay, i) for i in range(0, 7)]
    PlotJX(X, Y, title=title, xlabel=xlabel, ylabel=ylabel, fsize=fsize, filename=filename, rotation=rotation)


def PlotChart3(dic, filename=CHART3):
    x = []
    labels = []
    for i in dic:
        x.append(dic[i])
        labels.append(i)
    PlotXX(x, labels, xlabel="label name", ylabel="numbers of days", filename=filename)


def PlotProChart34(x, labels, xlabel="project name", ylabel="Issue Lifecycle", filename="ProChart34.jpg"):
    PlotXX(x, labels, xlabel=xlabel, ylabel=ylabel, filename=filename)


def PlotChart4(dic, filename=CHART4):
    x = []
    labels = []
    for i in dic:
        x.append(dic[i])
        labels.append(i)
    PlotXX(x, labels, xlabel="label name", ylabel="numbers of comments", filename=filename)


def PlotChart5(x, y, filename=CHART5):
    PlotXX(x, labels=y, xlabel="project name", ylabel="Member ratio", filename=filename)


def PlotChart6(x, y, filename=CHART6):
    PlotXX(x, labels=y, xlabel="project name", ylabel="member comments ratio", filename=filename)


def PlotChart7(x, y, filename=CHART7):
    PlotXX(x, labels=y, xlabel="project name", ylabel="user contributions number", filename=filename)


if __name__ == "__main__":
    x1 = ['2017-01', '2017-02', '2017-03', '2017-04', '2017-05', '2017-06', '2017-07', '2017-08',
          '2017-09', '2017-10', '2017-11', '2017-12']
    y1 = [0, 85, 84, 80, 75, 70, 70, 74, 78, 70, 74, 80]
    # PlotJX(x1,y1)
    PlotXX([y1], [x1[0]], xlabel="label name", ylabel="numbers of days", filename="1.jpg")

