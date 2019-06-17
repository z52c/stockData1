#coding=utf-8
import sqlite3
from daye import *


def makeStockDailyTable(code):
    '''
    创建用于保存指定股票每日交易数据的数据表
    '''
    conn = sqlite3.connect(dayDBFile)
    c = conn.cursor()
    sqlStr="CREATE TABLE day"+str(code)+" (date char(6),hprice REAL,lprice REAL,oprice REAL,cprice REAL,chg REAL,pchg REAL,turnover REAL,volume INTEGER,ema12 REAL,ema26 REAL,dif REAL,dea REAL);"
    c.execute(sqlStr)
    conn.commit()
    conn.close()
    print(code+'daily db table created!')


def makeStockWeekTable(code):
    '''
    创建用于保存指定股票每日交易数据的数据表
    '''
    conn = sqlite3.connect(weekDBFile)
    c = conn.cursor()
    sqlStr="CREATE TABLE week"+str(code)+" (date char(6),hprice REAL,lprice REAL,oprice REAL,cprice REAL,chg REAL,pchg REAL,turnover REAL,volume INTEGER,ema12 REAL,ema26 REAL,dif REAL,dea REAL);"
    c.execute(sqlStr)
    conn.commit()
    conn.close()
    print(code+'weekly db table created!')


def ifTableExist(dbName,tableName):
    '''
    判断指定数据库中指定的表是否存在
    '''
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    sqlStr="SELECT COUNT(*) FROM sqlite_master where type='table' and name='"+tableName+"'"
    cursor=c.execute(sqlStr)
    for a in cursor:
        if a[0] == 1:
            conn.close()
            return True
    conn.close()
    return False

def storeDailyDataWithMACD(code):
    '''
    从下载的csv文件中读取数据，计算出macd并且保存到数据库对应的表中
    '''
    dataList=[]
    dataList=getDailyDataFromCSV(code)
    tmpStr=dataList.pop()
    tmpList=tmpStr.split(',')
    dataList.reverse()
    conn = sqlite3.connect(dayDBFile)
    c = conn.cursor()
    for i in range(14):
        if tmpList[i] == 'None':
            tmpList[i]='0.0'
    sqlStr="INSERT INTO day"+str(code)+" VALUES (\""+tmpList[0]+"\","+tmpList[4]+","+tmpList[5]+","+tmpList[6]+","+tmpList[3]+","+"0.0"+","+"0.0"+","+tmpList[10]+","+tmpList[11]+",0,0,0,0);"
    c.execute(sqlStr)
    ema12=0.0
    ema26=0.0
    dif=0.0
    dea=0.0
    for x in dataList:
        tmpList=x.split(',')
        for i in range(14):
            if tmpList[i] == 'None':
                tmpList[i]='0.0'
        if tmpList[3]=='0.0':
            sqlStr="INSERT INTO day"+str(code)+" VALUES (\""+tmpList[0]+"\","+'0.0'+","+'0.0'+","+'0.0'+","+'0.0'+","+'0.0'+","+'0.0'+","+'0.0'+","+'0.0'+","+str(ema12)+","+str(ema26)+","+str(dif)+","+str(dea)+");"
            c.execute(sqlStr)
            continue
        ema12=ema12*11/13+float(tmpList[3])*2/13
        ema26=ema26*25/27+float(tmpList[3])*2/27
        dif=ema12-ema26
        dea=dea*8/10+dif*2/10
        sqlStr="INSERT INTO day"+str(code)+" VALUES (\""+tmpList[0]+"\","+tmpList[4]+","+tmpList[5]+","+tmpList[6]+","+tmpList[3]+","+tmpList[8]+","+tmpList[9]+","+tmpList[10]+","+tmpList[11]+","+str(ema12)+","+str(ema26)+","+str(dif)+","+str(dea)+");"
        c.execute(sqlStr)
    conn.commit()
    conn.close()


def dealOneWeekData(code,oneWeekDataList):
    '''
    仅在storeWeekDataWithMACD函数中使用
    处理传入的一周的每日数据
    返回一条周数据
    数据有可能小于5条
    若第一天没有开盘，则不能把第一天的开盘价(0)作为周开盘价，否则在计算涨跌幅时除数0会报错
    '''
    rtnList=[]
    flag=False
    date=oneWeekDataList[0][0]
    oprice=float(oneWeekDataList[0][3])
    if oprice == 0.0:
        flag=True
    hprice=float(oneWeekDataList[0][1])
    lprice=float(oneWeekDataList[0][2])
    turnover=0.0
    volume=0
    cprice=0.0
    for a in oneWeekDataList:
        if flag and a[3]!=0.0:
            oprice=a[3]
            flag=False
        if a[1]>hprice:
            hprice=float(a[1])
        if a[2]<lprice:
            lprice=float(a[2])
        turnover=turnover+float(a[7])
        volume=volume+int(a[8])
        cprice=float(a[4])
    chg=cprice-oprice
    if flag:
        pchg=0.0
    else:
        pchg=chg/oprice
    rtnList.append(date)
    rtnList.append(str(hprice))
    rtnList.append(str(lprice))
    rtnList.append(str(oprice))
    rtnList.append(str(cprice))
    rtnList.append(str(chg))
    rtnList.append(str(pchg))
    rtnList.append(str(turnover))
    rtnList.append(str(volume))
    return rtnList


def storeWeekDataWithMACDIntoDb(code,weekDataList):
    '''
    仅用于被storeWeekDataWithMACD函数调用
    将处理完毕的包含macd的周数据存入数据库
    '''
    conn = sqlite3.connect(weekDBFile)
    c = conn.cursor()
    for a in weekDataList:
        sqlStr="INSERT INTO week"+str(code)+" VALUES (\""+str(a[0])+"\","+str(a[1])+","+str(a[2])+","+str(a[3])+","+str(a[4])+","+str(a[5])+","+str(a[6])+","+str(a[7])+","+str(a[8])+","+str(a[9])+","+str(a[10])+","+str(a[11])+","+str(a[12])+");"
        c.execute(sqlStr)
    conn.commit()
    conn.close()
    print(code+'week data inserted!')


def storeWeekDataWithMACD(code):
    '''
    制作该股票的周数据，存入表中
    '''
    print(code +'week data begin!')
    dayDataList=[]
    weekDataList1=[]
    conn = sqlite3.connect(dayDBFile)
    sqlStr='SELECT *  from day'+str(code)
    c = conn.cursor()
    cursor = c.execute(sqlStr)
    for a in cursor:
        dayDataList.append(a)
    conn.close()
    if len(dayDataList)==0:
        print(code +'daily data in db file is empty!')
        return
    i=whatDay(dayDataList[0][0])
    tmpList=[]
    for a in dayDataList:
        if whatDay(a[0]) < i:
            i=whatDay(a[0])
            weekDataList1.append(dealOneWeekData(code,tmpList))
            tmpList.clear()
            tmpList.append(a)
        tmpList.append(a)
        i=whatDay(a[0])
    weekDataList1.append(dealOneWeekData(code,tmpList))
    ema12=0.0
    ema26=0.0
    dif=0.0
    dea=0.0
    weekDataList=[]
    for a in weekDataList1:
        ema12=ema12*11/13+float(a[4])*2/13
        ema26=ema26*25/27+float(a[4])*2/27
        dif=ema12-ema26
        dea=dea*8/10+dif*2/10
        a.append(ema12)
        a.append(ema26)
        a.append(dif)
        a.append(dea)
        weekDataList.append(a)
    makeStockWeekTable(code)
    storeWeekDataWithMACDIntoDb(code,weekDataList)


def getAllData(type,code):
    '''
    返回该股票所有的数据
    type 1 day  2 week
    '''
    rtnList=[]
    if type == 1:
        conn = sqlite3.connect(dayDBFile)
        sqlStr='SELECT *  from day'+str(code)
        c = conn.cursor()
        cursor = c.execute(sqlStr)
        for a in cursor:
            rtnList.append(a)
        conn.close()
        return rtnList
    else:
        conn = sqlite3.connect(weekDBFile)
        sqlStr='SELECT *  from week'+str(code)
        c = conn.cursor()
        cursor = c.execute(sqlStr)
        for a in cursor:
            rtnList.append(a)
        conn.close()
        return rtnList
