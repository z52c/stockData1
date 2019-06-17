#coding=utf-8
from download import *
from daye import *
from db import *
import threading

threadLock = threading.Lock()
stockList=[]


def getDailyDataWithMACD(code):
    '''
    从文件中读取全部每日数据，计算出macd，存入数据库
    仅在第一次使用
    '''
    if not ifTableExist(dayDBFile,'day'+str(code)):
        downloadAllDayData(code)
        if not isDataEmpty(str(code)):
            makeStockDailyTable(code)
            storeDailyDataWithMACD(code)

def perStockJob(threadName):
    global stockList
    threadLock.acquire()
    while(len(stockList)>0):
        stockCode=stockList.pop()
        threadLock.release()
        getDailyDataWithMACD(stockCode)
        threadLock.acquire()
    threadLock.release()

class stockThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print ("开启stock线程： " + self.name)
        perStockJob(self.name)
        print ("结束stock线程： " + self.name)

def doDailyDataJob():
    '''
    获取全部股票的全部日交易数据
    '''
    th=[]
    global stockList
    stockList=getStockList()
    print(stockList)
    for i in range(15):
        t = stockThread(i, "Thread-%d" %i)
        t.start()
        th.append(t)
    for t in th:
        t.join()
    print('结束')

def weeklyJob():
    stockList=getStockList()
    for a in stockList:
        if not ifTableExist(weekDBFile,'week'+a) and ifTableExist(dayDBFile,'day'+a):
            storeWeekDataWithMACD(a)

def getJinchaData(code):
    signal1=False
    signal2=False
    data=getAllData(2,code)
    rtnList=[]
    for a in data:
        if not signal1:
            if float(a[11])<float(a[12]):
                signal1=True
        elif not signal2:
            if float(a[11])>float(a[12]):
                signal2=True
                rtnList.append(a[0])
        else:
            signal1=False
            signal2=False
    return rtnList

def tmp():
    stockList=getStockList()
    for a in stockList:
        if ifTableExist(weekDBFile,'week'+a):
            tmpList=getJinchaData(a)
            lastDate=tmpList.pop()
            #lastDate2=tmpList.pop()
            turnover=0.0
            data=getAllData(2,a)
            data.reverse()
            while True:
                b=data.pop()
                if b[0]==lastDate:
                    break
            for i in data:
                turnover=turnover+float(b[7])
            if turnover > 200.0:
                print(str(a)+lastDate)



if __name__ == '__main__':
    tmp()
