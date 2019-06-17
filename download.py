#coding=utf-8
from urllib import request
from daye import *


def downloadDayData(code,startDate,endDate):
    '''
    下载指定日期之间的交易数据,保存到临时目录下，以股票代码作为名称，后缀.csv
    http://quotes.money.163.com/service/chddata.html?code=0601398&start=20140720&end=20150508
    '''
    code=str(code)
    if(code[0] == '6'):
        codeStr='0'+str(code)
    else:
        codeStr='1'+str(code)
    url='http://quotes.money.163.com/service/chddata.html?code='+codeStr+'&start='+startDate+'&end='+endDate
    request.urlretrieve(url, tmpFolder+code+'.csv')
#    print(str(code)+'csv downloaded between 'startDate+' and '+endDate)

def downloadAllDayData(code):
    '''
    下载指定股票的所有交易数据,保存到临时目录下，以股票代码作为名称，后缀.csv
    http://quotes.money.163.com/service/chddata.html?code=0601398
    '''
    code=str(code)
    if(code[0] == '6'):
        codeStr='0'+str(code)
    else:
        codeStr='1'+str(code)
    url='http://quotes.money.163.com/service/chddata.html?code='+codeStr
    #fileName=code+'.csv'
    request.urlretrieve(url, tmpFolder+code+'.csv')
    print(str(code)+'csv all data downloaded')

def getStockList():
    '''
    来源东方财富
    http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery112404305072274467552_1560642107545&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOIATC&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)%7D)&cmd=C._A&st=(ChangePercent)&sr=-1&p=1&ps=4000
    '''
    rtnList=[]
    url="http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery112404305072274467552_1560642107545&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOIATC&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)%7D)&cmd=C._A&st=(ChangePercent)&sr=-1&p=1&ps=4000"
    response=request.urlopen(url)
    data=response.read()
    data=str(data)
    begin=data.find('[')
    end=data.find(']')
    data=data[begin+1:end]
    DataList=eval(data)
    for a in DataList:
        tmpList=a.split(',')
        if tmpList[3]=='-':
            continue
        rtnList.append(tmpList[1])
    print('em data stockList got ,length: ' +str(len(rtnList)))
    return rtnList
