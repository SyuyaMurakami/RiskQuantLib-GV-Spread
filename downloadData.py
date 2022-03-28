#!/usr/bin/python
# coding = utf-8
import os
import sys

import pandas as pd

from RiskQuantLib.Module import *
path = sys.path[0]

def downloadData():
    from RiskQuantLib.DataInputAPI.getDataFromWind import getOptionMarketData,getAllStockOfSector,getSHIBOR
    from RiskQuantLib.Tool.strTool import getLastTradingDate,generateTradingDateList,changeSecurityListToStr
    today = pd.Timestamp.now()
    lastTradingDay = getLastTradingDate(today)
    # 更新期权数据
    df = pd.read_csv(path+os.sep+'options.csv',converters={'DATE':pd.Timestamp})
    latestUpdateDate = pd.Timestamp(max(df['DATE']))
    updateList = generateTradingDateList(latestUpdateDate,lastTradingDay)
    if updateList[-1] != latestUpdateDate:
        callSectorCode = '1000018861000000'
        putSectorCode = '1000018862000000'
        updateDFList = []
        for i in updateList:
            callOptionCode = getAllStockOfSector(i,callSectorCode)
            putOptionCode = getAllStockOfSector(i, putSectorCode)
            optionCode = callOptionCode['wind_code'].to_list()+putOptionCode['wind_code'].to_list()
            dayInfo = getOptionMarketData(changeSecurityListToStr(optionCode),i)
            updateDFList.append(dayInfo)
            print("Finish Download : ",i)
        updateDF = pd.concat(updateDFList)
        if not updateDF.empty:
            tmp = pd.concat([df,updateDF])
            tmp['DATE'] = [i.strftime("%Y/%m/%d") for i in tmp['DATE']]
            tmp.to_csv(path + os.sep + 'options.csv', index=None)
            print("Option Data Download Finished")

    # 更新日期
    df = pd.read_csv(path + os.sep + 'tradeday.csv',converters={'DateTime':pd.Timestamp})
    latestUpdateDate = pd.Timestamp(max(df['DateTime']))
    updateList = generateTradingDateList(latestUpdateDate,lastTradingDay)
    if len(updateList)!=0:
        updateDate = pd.DataFrame(updateList[1:],columns=['DateTime'])
        df = pd.concat([df,updateDate])
        df['DateTime'] = [i.strftime("%Y/%m/%d") for i in df['DateTime']]
        df.to_csv(path + os.sep + 'tradeday.csv', index=None)
    print("Download Trade Day Finish")

    # 更新SHIBOR
    df = pd.read_csv(path + os.sep + 'shibor.csv',index_col=0)
    latestUpdateDate = pd.Timestamp(max([pd.Timestamp(i) for i in df.index]))
    updateList = generateTradingDateList(latestUpdateDate,lastTradingDay)
    for i in updateList:
        tmp = getSHIBOR(i)
        df.loc[i.strftime("%Y-%m-%d")] = tmp['CLOSE'].to_list()
    df.sort_index(ascending=False,inplace=True)
    df.to_csv(path + os.sep + 'shibor.csv')
    print("Download SHIBOR Finish")

    print("Download Data Finish")