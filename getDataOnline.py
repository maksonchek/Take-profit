import csv
import pandas as pd
import time
import datetime
from moexalgo import Ticker
import getDataTradeStats
import getDataOrderStats

#получаем свечи за указанный период и в указанном формате period
def getCandles(start, end, tickers, period='D') -> pd.DataFrame:
   df = pd.DataFrame({'ticker': [],
                      'open': [],
                      'close': [],
                      'high': [],
                      'low': [], 
                      'value': [],
                      'volume': [],
                      'begin': [],
                      'end': []})
   
   for ticker in tickers:
      ticker_moex = Ticker(ticker)
      c = ticker_moex.candles(date=start, till_date=end, period=period)
      
      arr = []
      for one in c:
         arr = [ticker, one.open, one.close, one.high, one.low, one.value, one.volume, one.begin, one.close]
         df.loc[len(df.index)] = arr
      
      time.sleep(0.5) 
   
   print("Данные о свечах получены")   
   return df    

def getOnlineDataOrderStats(tickers=None, filename = None):
        onlineData = pd.DataFrame()
        #k = 0
        #for date in dates:
        if tickers is not None:
                for ticker in tickers:
                        url = f'https://iss.moex.com/iss/datashop/algopack/eq/orderstats/{ticker}.csv?iss.only=data&latest=1'
                        df = pd.read_csv(url, sep=';', skiprows=2)
                        orderstats = pd.concat([orderstats, df])
                        print("получил " + str(ticker))
                        time.sleep(0.5)
        else:
                        url = f'https://iss.moex.com/iss/datashop/algopack/eq/orderstats.csv?iss.only=data&latest=1'
                        df = pd.read_csv(url, sep=';', skiprows=2)
                        orderstats = pd.concat([orderstats, df])
                        
                        print("получил")            
                        time.sleep(0.5)                
                 
        # k += 1 
        # if k % 3 == 0:
        
        if filename is not None:               
                orderstats.to_csv(filename, index=None, sep=";")
                
        print('данные о статиске заявок за последние 5 минут получены')
        
        return orderstats
     
def getOnlineDataTradeStats(tickers=None, filename = None) -> pd.DataFrame:
        #dates = getDateRange(date1, date2)
        tradestats = pd.DataFrame()
        #k = 0
        #for date in dates:
        if tickers is not None:
                for ticker in tickers:
                        url = f'https://iss.moex.com/iss/datashop/algopack/eq/tradestats/{ticker}.csv?iss.only=data&latest=1'
                        df = pd.read_csv(url, sep=';', skiprows=2)
                        tradestats = pd.concat([tradestats, df])
                        print("получил " + str(ticker))
                        time.sleep(0.5)
        else:
                        url = f'https://iss.moex.com/iss/datashop/algopack/eq/tradestats.csv?iss.only=data&latest=1'
                        df = pd.read_csv(url, sep=';', skiprows=2)
                        tradestats = pd.concat([tradestats, df])
                        
                        print("получил")        
                        time.sleep(0.5)                
                 
        # k += 1 
        # if k % 3 == 0:
                
        if filename is not None:               
                tradestats.to_csv(filename, index=None, sep=";")
        print('данные о статистике торгов за последние 5 минут получены')
        
        return tradestats     

def start(tickers):
   
   now_day = datetime.date.today() #сегодня
   
   #now_day = datetime.date(2023, 12, 8)
   
   yesterday = now_day - datetime.timedelta(days=1) #вчера
   
   week = yesterday - datetime.timedelta(days=7) #неделя от вчерашнего дня
   
   week_candle:pd.DataFrame = getCandles(yesterday, week, tickers, 'D') #свечи по интересущим нас тикерам за неделю
   
   #получаем и агрегируем данные за сегодняшний день о статистике торгов
   tradeStats_today:pd.DataFrame = getDataTradeStats.getDataTicker(None, now_day, now_day)
   hourTradeStats_today:list = getDataTradeStats.getDataHourTradeStats(tradeStats_today, True, tickers)
   
   #получаем и агрегируем данные за сегодняшний день о статистике заявок
   orderStats_today:pd.DataFrame = getDataOrderStats.getDataTicker(None, now_day, now_day)
   hourOrderStats_today:list = getDataOrderStats.getDataHourOrderStats(orderStats_today, True, tickers)
   
   #получаем агрегированные данные за последний час о статистике торгов
   lastHourTradeStats:list = hourTradeStats_today[-len(tickers):]
   print(lastHourTradeStats)
   
   #получаем агрегированные данные за последний час о статистике заявок
   lastHourOrderStats:list = hourOrderStats_today[-len(tickers):]
   print(lastHourOrderStats)
   
   
   #если алгоритм запущен ночью и получены данные не за сегодня
   if datetime.datatime.strptime(lastHourTradeStats[0][0], '%Y %m %d') != now_day:
         lastHourTradeStats = []
         lastHourOrderStats = []
         
   while True:
      nowTradeStats = getOnlineDataTradeStats(tickers).values.tolist()   
      nowOrderStats = getOnlineDataOrderStats(tickers).values.tolist()  
      
      if len(lastHourTradeStats) == 0:
         lastHourTradeStats = nowTradeStats
         lastHourOrderStats = nowOrderStats
         
         #здесб продолжить, нужно добавить корректное время и обрабатывать
      else: #если данные какие то уже есть за последний час
            
         
      
      
         
            
    

if __name__ == '__main__':
   tickers = ['SBER', 'GAZP', 'ROSN', 'NVTK', 'GMKN', 'YNDX', 'LKOH', 'PLZL', 'MOEX', 'PHOR']
   
   start(tickers)



                  