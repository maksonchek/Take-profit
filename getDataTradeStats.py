import csv
import pandas as pd
import time
import datetime

def getDateRange(date1, date2):
        numdays = (date2 - date1).days + 1

        dateList = [str((date1 + datetime.timedelta(days=x)).strftime('%Y-%m-%d')) for x in range(numdays)]

        return dateList

def getDataTicker(tickers, date1, date2, filename):
        #dates = getDateRange(date1, date2)
        tradestats = pd.DataFrame()
        #k = 0
        #for date in dates:
        if tickers is not None:
                for ticker in tickers:
                        url = f'https://iss.moex.com/iss/datashop/algopack/eq/tradestats/{ticker}.csv?from={date1}&till={date2}&iss.only=data'
                        df = pd.read_csv(url, sep=';', skiprows=2)
                        tradestats = pd.concat([tradestats, df])
                        print("получил" + str(ticker))
                        time.sleep(0.5)
        else:
                for cursor in range(25):
                        url = f'https://iss.moex.com/iss/datashop/algopack/eq/tradestats.csv?from={date1}&till={date2}&start={cursor*1000}&iss.only=data'
                        df = pd.read_csv(url, sep=';', skiprows=2)
                        tradestats = pd.concat([tradestats, df])
                        if df.shape[0] < 1000:
                                break
        
                        time.sleep(0.5)                
                 
        # k += 1 
        # if k % 3 == 0:
                       
        tradestats.to_csv(filename, index=None, sep=";")
        print('данные получены')


def getDataHourTradeStats(filename, tickers=None):
        with open(filename, 'r') as tradestats:
                readtradestats = csv.reader(tradestats, delimiter=";")
                titles = next(readtradestats)
                data = list(readtradestats)

        new_data = [titles]
        hashtab = {}  
        index = 1    
        #пробегаемся по каждой строчке списка       
        for share in data:
                #тикер акции
                ticker = share[2]
                if tickers is None or ticker in tickers:
                        if ticker not in hashtab:
                                hashtab[ticker] = [index, 0]
                                new_data.append(share)
                                time_beg = datetime.datetime.strptime(new_data[-1][1], "%H:%M:%S")
                                hours = time_beg.replace(minute=0, second=0, microsecond=0)
                                new_data[-1][1] = str(hours.strftime("%H:%M:%S"))
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

                                prev_time = new_data[index_of_share][0] + " " + new_data[index_of_share][1]
                                prev_time = datetime.datetime.strptime(prev_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(minutes=5)

                                cur_time = share[0] + " " + share[1]
                                cur_time = datetime.datetime.strptime(cur_time, "%Y-%m-%d %H:%M:%S")

                                time_diff = cur_time - prev_time
                                #создаём новую строку для следующего часа
                                if time_diff.total_seconds() >= 3600:
                                        hashtab[ticker] = [index, 0]
                                        new_data.append(share)
                                        time_beg = datetime.datetime.strptime(new_data[-1][1], "%H:%M:%S")
                                        hours = time_beg.replace(minute=0, second=0, microsecond=0)
                                        new_data[-1][1] = str(hours.strftime("%H:%M:%S"))
                                        index += 1          

        outputfile = "hour" + filename
        with open(outputfile, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile, delimiter=';')
                csv_writer.writerows(new_data)

        print("Файл " + outputfile + " записан")

        return new_data

def joinCsv(filename1: str, filename2: str) -> None:
        df1 = pd.read_csv(filename1, sep=";")
        df1 = df1.dropna(axis=0, how='all')
        df1 = df1.dropna(axis=1, how='all')
        df2 = pd.read_csv(filename2, sep=";")
        df2 = df2.dropna(axis=0, how='all')
        df2 = df2.dropna(axis=1, how='all')

        combined_df = pd.concat([df1, df2], ignore_index=True)

        combined_df.to_csv(filename1, index=False, sep=";")

if __name__ == "__main__":
        filenames = ['tradestats_2020.csv', 'tradestats_2021.csv', 'tradestats_2022.csv', 'tradestats_2023.csv', 'tradestats_2023_rem.csv']
        tickers = ['SBER', 'GAZP', 'ROSN', 'NVTK', 'GMKN', 'YNDX', 'LKOH', 'PLZL', 'MOEX', 'PHOR']
        #getDataTicker(tickers, datetime.date(2022, 10, 1), datetime.date(2023, 10, 31), filename)

        with open(filenames[0], 'r') as tradestats:
                readtradestats = csv.reader(tradestats, delimiter=";")
                titles = next(readtradestats)

        with open('hourtradestats-2020-2023.csv', 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile, delimiter=';')
                csv_writer.writerow(titles)

        getDataTicker(None, datetime.date(2023, 11, 1), datetime.date(2023, 12, 8), filenames[-1])

        for filename in filenames:
                getDataHourTradeStats(filename, tickers)
                joinCsv('hourtradestats-2020-2023.csv', "hour" + filename)      
