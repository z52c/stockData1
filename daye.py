#coding=utf-8
import time
import datetime

tmpFolder='tmp//'
dayDBFile='day.db'
weekDBFile='week.db'

def whatDay(dateStr):
    '''
    输入2019-06-13格式的字符串，返回周几
    '''
    dateSplitList=dateStr.split('-')
    year=dateSplitList[0]
    month=dateSplitList[1]
    day=dateSplitList[2]
    return datetime.datetime(int(year), int(month), int(day), 0, 0, 0, 0).weekday()+1

def isDataEmpty(code):
    '''
    判断下载的文件是否无数据
    '''
    f=open(tmpFolder+str(code)+'.csv','r')
    line=f.readline()
    line=f.readline()
    f.close()
    if(len(line)==0):
        return True
    else:
        return False

def getDailyDataFromCSV(code):
    '''
    读取下载文件中的股票数据，以列表的形式返回数据
    '''
    tmpList=[]
    f=open(tmpFolder+str(code)+'.csv','r')
    line=f.readline()
    while True:
        line=f.readline()
        if not line:
            break
        tmpList.append(line)
    return tmpList
