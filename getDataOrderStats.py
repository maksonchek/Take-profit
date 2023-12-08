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
        orderstats = pd.DataFrame()
        #k = 0
        #for date in dates:
        if tickers is not None:
                for ticker in tickers:
                        url = f'https://iss.moex.com/iss/datashop/algopack/eq/orderstats/{ticker}.csv?from={date1}&till={date2}&iss.only=data'
                        df = pd.read_csv(url, sep=';', skiprows=2)
                        orderstats = pd.concat([orderstats, df])
                        print("получил" + str(ticker))
                        time.sleep(0.5)
        else:
                for cursor in range(25):
                        url = f'https://iss.moex.com/iss/datashop/algopack/eq/orderstats.csv?from={date1}&till={date2}&start={cursor*1000}&iss.only=data'
                        df = pd.read_csv(url, sep=';', skiprows=2)
                        orderstats = pd.concat([orderstats, df])
                        if df.shape[0] < 1000:
                                break
        
                        time.sleep(0.5)                
                 
        # k += 1 
        # if k % 3 == 0:
                       
        orderstats.to_csv(filename, index=None, sep=";")
        print('данные получены')

def getDataHourOrderStats(filename, tickers=None):
        with open(filename, 'r') as orderstats:
                readorderstats = csv.reader(orderstats, delimiter=";")
                titles = next(readorderstats)
                data = list(readorderstats)

        new_data = [titles]
        hashtab = {}  
        index = 1    
        #пробегаемся по каждой строчке списка       
        for share in data:
                #тикер акции
                ticker = share[2]
                if tickers is None or ticker in tickers:
                        if ticker not in hashtab:
                                hashtab[ticker] = index
                                new_data.append(share)
                                time_beg = datetime.datetime.strptime(new_data[-1][1], "%H:%M:%S")
                                hours = time_beg.replace(minute=0, second=0, microsecond=0)
                                new_data[-1][1] = str(hours.strftime("%H:%M:%S"))
                                index += 1
                        else:
                                #находим индекс акции
                                index_of_share = hashtab[ticker]

                                # put_orders_b;
                                new_data[index_of_share][3] = float(new_data[index_of_share][3]) + float(share[3])

                                # put_orders_s;
                                new_data[index_of_share][4] = float(new_data[index_of_share][4]) + float(share[4])

                                # put_val_b;
                                new_data[index_of_share][5] = float(new_data[index_of_share][5]) + float(share[5])

                                # put_val_s;
                                new_data[index_of_share][6] = float(new_data[index_of_share][6]) + float(share[6])

                                # put_vol_b;
                                new_data[index_of_share][7] = float(new_data[index_of_share][7]) + float(share[7])

                                # put_vol_s;
                                new_data[index_of_share][8] = float(new_data[index_of_share][8]) + float(share[8])

                                # put_vwap_b средневзвешенная цена - вредный признак
                        
                                # put_vwap_s средневзвешенная цена - вредный признак
                        
                                # put_vol;
                                new_data[index_of_share][11] = float(new_data[index_of_share][11]) + float(share[11])
                        
                                # put_val;
                                new_data[index_of_share][12] = float(new_data[index_of_share][12]) + float(share[12])
                        
                                # put_orders;
                                new_data[index_of_share][13] = float(new_data[index_of_share][13]) + float(share[13])
                        
                                # cancel_orders_b;
                                new_data[index_of_share][14] = float(new_data[index_of_share][14]) + float(share[14])
                        
                                # cancel_orders_s;
                                new_data[index_of_share][15] = float(new_data[index_of_share][15]) + float(share[15])
                        
                                # cancel_val_b;
                                new_data[index_of_share][16] = float(new_data[index_of_share][16]) + float(share[16])
                        
                                # cancel_val_s;
                                new_data[index_of_share][17] = float(new_data[index_of_share][17]) + float(share[17])
                        
                                # cancel_vol_b;
                                new_data[index_of_share][18] = float(new_data[index_of_share][18]) + float(share[18])
                        
                                # cancel_vol_s;
                                new_data[index_of_share][19] = float(new_data[index_of_share][19]) + float(share[19])
                        
                                # cancel_vwap_b;cancel_vwap_s; средневзвешенная цена - вредный признак
                        
                                # cancel_vol;
                                new_data[index_of_share][22] = float(new_data[index_of_share][22]) + float(share[22])
 
                                # cancel_val;
                                new_data[index_of_share][23] = float(new_data[index_of_share][23]) + float(share[23])
 
                                # cancel_orders;
                                new_data[index_of_share][24] = float(new_data[index_of_share][24]) + float(share[24])
                        
                                # SYSTIME      

                                #создаём новую строку для следующего часа
                                prev_time = new_data[index_of_share][0] + " " + new_data[index_of_share][1]
                                prev_time = datetime.datetime.strptime(prev_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(minutes=5)

                                cur_time = share[0] + " " + share[1]
                                cur_time = datetime.datetime.strptime(cur_time, "%Y-%m-%d %H:%M:%S")

                                time_diff = cur_time - prev_time
                                #создаём новую строку для следующего часа
                                if time_diff.total_seconds() >= 3600:
                                        hashtab[ticker] = index
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
        filenames = ['orderstats_2020.csv', 'orderstats_2021.csv', 'orderstats_2022.csv', 'orderstats_2023.csv', 'orderstats_2023_rem.csv']
        tickers = ['SBER', 'GAZP', 'ROSN', 'NVTK', 'GMKN', 'YNDX', 'LKOH', 'PLZL', 'MOEX', 'PHOR']
        #getDataTicker(tickers, datetime.date(2022, 10, 1), datetime.date(2023, 10, 31), filename)

        with open(filenames[0], 'r') as orderstats:
                readorderstats = csv.reader(orderstats, delimiter=";")
                titles = next(readorderstats)

        with open('hourorderstats-2020-2023.csv', 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile, delimiter=';')
                csv_writer.writerow(titles)

        getDataTicker(None, datetime.date(2023, 11, 1), datetime.date(2023, 12, 8), filenames[-1])

        for filename in filenames:
                #getDataHourOrderStats(filename, tickers)
                joinCsv('hourorderstats-2020-2023.csv', "hour" + filename)