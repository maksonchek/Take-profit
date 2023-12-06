import csv
import pandas as pd
import time
import datetime

def getDateRange(date1, date2):
        numdays = (date2 - date1).days + 1

        dateList = [str((date1 + datetime.timedelta(days=x)).strftime('%Y-%m-%d')) for x in range(numdays)]

        return dateList

def getDataTicker(tickers, date1, date2, filename):
        dates = getDateRange(date1, date2)
        tradestats = pd.DataFrame()
        k = 0
        for date in dates:
                for ticker in tickers:
                        url = f'https://iss.moex.com/iss/datashop/algopack/eq/tradestats/{ticker}.csv?from={date}&till={date}&iss.only=data'
                        df = pd.read_csv(url, sep=';', skiprows=2)
                        tradestats = pd.concat([tradestats, df])
                        time.sleep(0.5)

                k += 1 
                if k == 3:
                        print("работаю")
                        k = 0       
    
        tradestats.to_csv(filename, index=None)
        print('данные получены')

def getDataHourTradeStats(filename):
        with open(filename, 'r') as tradestats:
                readtradestats = csv.reader(tradestats, delimiter=",")
                titles = next(readtradestats)
                data = list(readtradestats)

        print(data[167])
        new_data = [titles]
        hashtab = {}  
        index = 1    
        #пробегаемся по каждой строчке списка       
        for share in data:
                #тикер акции
                ticker = share[2]
                if ticker not in hashtab:
                        hashtab[ticker] = [index, 0]
                        new_data.append(share)
                        index += 1
                else:
                        #находим индекс акции
                        index_of_share = hashtab[ticker][0]
                        #увеличиваем счетчик промежутков
                        hashtab[ticker][1] += 1

                        #pr_high
                        try:
                                new_data[index_of_share][4] = max(float(new_data[index_of_share][4]), float(share[4]))
                        except:
                               print("pr_high")
                               save1 = data.index(share)
                               print(data[save1]) 

                        #pr_low
                        new_data[index_of_share][5] = min(float(new_data[index_of_share][5]), float(share[5]))

                        #если промежутков 12, значит закрыли час
                        #if hashtab[ticker][1] == 12:
                        #pr_close
                        new_data[index_of_share][6] = float(share[6])

                        #share[7] pr_std - станадртное отклонение цены, вредный признак

                        #vol
                        new_data[index_of_share][8] = float(new_data[index_of_share][8]) + float(share[8])

                        #val
                        new_data[index_of_share][9] = float(new_data[index_of_share][9]) + float(share[9])

                        #trades
                        new_data[index_of_share][10] = float(new_data[index_of_share][10]) + float(share[10])

                        #share[11] pr_vwap - средневзвешенная цена - вредный признак

                        #pr_change
                        try:
                                pr_open = float(new_data[index_of_share][3])
                                pr_close = float(new_data[index_of_share][6])
                                new_data[index_of_share][12] = (pr_close - pr_open) * 100 / pr_open
                        except:
                                print(ticker)
                                save1 = data.index(share)
                                print(save1)

                        

                        #trades_b
                        new_data[index_of_share][13] = float(new_data[index_of_share][13]) + float(share[13])

                        #trades_s
                        new_data[index_of_share][14] = float(new_data[index_of_share][14]) + float(share[14])

                        #val_b
                        new_data[index_of_share][15] = float(new_data[index_of_share][15]) + float(share[15])

                        #val_s
                        new_data[index_of_share][16] = float(new_data[index_of_share][16]) + float(share[16])

                        #vol_b
                        new_data[index_of_share][17] = float(new_data[index_of_share][17]) + float(share[17])

                        #vol_s
                        new_data[index_of_share][18] = float(new_data[index_of_share][18]) + float(share[18])

                        #disb
                        vol_b = float(new_data[index_of_share][17])
                        vol_s = float(new_data[index_of_share][18])
                        if vol_b != 0:
                                new_data[index_of_share][19] = vol_s / vol_b
                        else:
                                new_data[index_of_share][19] = float(100)        

                        #share[20] pr_vwap_b - средневзвешенная цена - вредный признак

                        #share[21] pr_vwap_s - средневзвешенная цена - вредный признак
                        #SYSTIME

                        #создаём новую строку для следующего часа
                        if hashtab[ticker][1] == 12:
                                hashtab[ticker] = [index, 0]
                                new_data.append(share)
                                index += 1          

        outputfile = "hour" + filename
        with open(outputfile, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile, delimiter=';')
                csv_writer.writerows(new_data)

        return new_data


if __name__ == "__main__":
        filename = 'tradestats_2022-2023.csv'
        tickers = ['SBER', 'GAZP', 'ROSN', 'NVTK', 'GMKN', 'YNDX', 'LKOH', 'PLZL', 'MOEX', 'PHOR']
        #getDataTicker(tickers, datetime.date(2022, 10, 1), datetime.date(2023, 10, 31), filename)
        getDataHourTradeStats(filename)
