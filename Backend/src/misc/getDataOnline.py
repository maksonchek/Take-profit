import csv
import pandas as pd
import time
import datetime
from moexalgo import Ticker
from misc import getDataTradeStats
from misc import getDataOrderStats

# получаем свечи за указанный период и в указанном формате period


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
            arr = [ticker, one.open, one.close, one.high, one.low,
                   one.value, one.volume, one.begin, one.end]
            df.loc[len(df.index)] = arr

        time.sleep(0.5)

    df = df.sort_values('begin')
    print("Данные о свечах получены")
    return df


def getOnlineDataOrderStats(tickers=None, filename=None):
    orderstats = pd.DataFrame()
    # k = 0
    # for date in dates:
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


def getOnlineDataTradeStats(tickers=None, filename=None) -> pd.DataFrame:
    # dates = getDateRange(date1, date2)
    tradestats = pd.DataFrame()
    # k = 0
    # for date in dates:
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


def start(tickers, day_stop):
    titles_tradeStats = ['tradedate',
                         'tradetime',
                         'secid',
                         'pr_open',
                         'pr_high',
                         'pr_low',
                         'pr_close',
                         'pr_std',
                         'vol',
                         'val',
                         'trades',
                         'pr_vwap',
                         'pr_change',
                         'trades_b',
                         'trades_s',
                         'val_b',
                         'val_s',
                         'vol_b',
                         'vol_s',
                         'disb',
                         'pr_vwap_b',
                         'pr_vwap_s',
                         'SYSTIME']

    titles_orderStats = ['tradedate',
                         'tradetime',
                         'secid',
                         'put_orders_b',
                         'put_orders_s',
                         'put_val_b',
                         'put_val_s',
                         'put_vol_b',
                         'put_vol_s',
                         'put_vwap_b',
                         'put_vwap_s',
                         'put_vol',
                         'put_val',
                         'put_orders',
                         'cancel_orders_b',
                         'cancel_orders_s',
                         'cancel_val_b',
                         'cancel_val_s',
                         'cancel_vol_b',
                         'cancel_vol_s',
                         'cancel_vwap_b',
                         'cancel_vwap_s',
                         'cancel_vol',
                         'cancel_val',
                         'cancel_orders',
                         'SYSTIME']

    now_day = datetime.date.today()  # сегодня
    # now_day = datetime.date(2023, 12, 3)
    save_date = None
    save_time = None
    while flag:  # now_day < day_stop:
        now_day = datetime.date.today()  # сегодня

        now_time = datetime.datetime.now().time()
        now_time = datetime.time(
            now_time.hour, now_time.minute, now_time.second)

        if now_day != save_date or save_date is None:

            # now_day = datetime.date(2023, 12, 8)
            now_day = datetime.date.today()  # сегодня

            yesterday = now_day - datetime.timedelta(days=1)  # вчера

            # неделя от вчерашнего дня
            week = yesterday - datetime.timedelta(days=7)

            # свечи по интересущим нас тикерам за неделю
            week_candle: pd.DataFrame = getCandles(
                yesterday, week, tickers, 'D')

            print("Отдали Максу свечи")
            # отдаем Максу return week_candle

            # получаем и агрегируем данные за сегодняшний день о статистике торгов
            tradeStats_today: pd.DataFrame = getDataTradeStats.getDataTicker(
                None, now_day, now_day)
            hourTradeStats_today: list = getDataTradeStats.getDataHourTradeStats(
                tradeStats_today, True, tickers)

            # получаем и агрегируем данные за сегодняшний день о статистике заявок
            orderStats_today: pd.DataFrame = getDataOrderStats.getDataTicker(
                None, now_day, now_day)
            hourOrderStats_today: list = getDataOrderStats.getDataHourOrderStats(
                orderStats_today, True, tickers)

            # получаем агрегированные данные за последний час о статистике торгов
            lastHourTradeStats: list = hourTradeStats_today[-len(tickers):]

            # получаем агрегированные данные за последний час о статистике заявок
            lastHourOrderStats: list = hourOrderStats_today[-len(tickers):]

            save_date = now_day

        # если алгоритм запущен ночью и получены данные не за сегодня
        # if datetime.datatime.strptime(lastHourTradeStats[0][0], '%Y %m %d') != now_day:
        #         lastHourTradeStats = []
        #         lastHourOrderStats = []

        # получаем онлайн данные
        nowTradeStats = getOnlineDataTradeStats(tickers).values.tolist()
        nowOrderStats = getOnlineDataOrderStats(tickers).values.tolist()

        last_data_time = datetime.datetime.strptime(
            nowTradeStats[0][1], "%H:%M:%S").time()
        if last_data_time != save_time or save_time is None:
            # Проверка на новый час
            if len(lastHourOrderStats[0][0]) != 0:
                prev_time = lastHourOrderStats[0][0] + \
                    " " + lastHourOrderStats[0][1]
                prev_time = datetime.datetime.strptime(
                    prev_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(minutes=5)
                cur_time = nowOrderStats[0][0] + " " + nowOrderStats[0][1]
                cur_time = datetime.datetime.strptime(
                    cur_time, "%Y-%m-%d %H:%M:%S")
                time_diff = cur_time - prev_time
                save_time = last_data_time

            else:
                time_diff = datetime.timedelta(hours=1, seconds=1)
            # начался новый час
            if time_diff.total_seconds() >= 3600:
                if lastHourTradeStats[0] == titles_tradeStats:
                    lastHourTradeStats.pop(0)
                if lastHourOrderStats[0] == titles_orderStats:
                    lastHourOrderStats.pop(0)

                # lastHourTradeStats = pd.DataFrame(
                #     (lastHourTradeStats + nowTradeStats), columns=titles_tradeStats)
                # lastHourOrderStats = pd.DataFrame(
                #     (lastHourOrderStats + nowOrderStats), columns=titles_orderStats)
                if len(lastHourTradeStats[0] != 0):
                    print("Отдали Максу статистику")
                # отдать Максу return lastHourTradeStats, lastHourOrderStats

                lastHourTradeStats = nowTradeStats
                lastHourOrderStats = nowOrderStats
                for x in lastHourTradeStats:
                    time_beg = datetime.datetime.strptime(x[1], "%H:%M:%S")
                    hours = time_beg.replace(minute=0, second=0, microsecond=0)
                    x[1] = str(hours.strftime("%H:%M:%S"))

                for x in lastHourOrderStats:
                    time_beg = datetime.datetime.strptime(x[1], "%H:%M:%S")
                    hours = time_beg.replace(minute=0, second=0, microsecond=0)
                    x[1] = str(hours.strftime("%H:%M:%S"))
            else:
                if lastHourTradeStats[0] == titles_tradeStats:
                    lastHourTradeStats.pop(0)
                if lastHourOrderStats[0] == titles_orderStats:
                    lastHourOrderStats.pop(0)

                lastHourTradeStats = pd.DataFrame(
                    (lastHourTradeStats + nowTradeStats), columns=titles_tradeStats)
                lastHourOrderStats = pd.DataFrame(
                    (lastHourOrderStats + nowOrderStats), columns=titles_orderStats)

                lastHourTradeStats: list = getDataTradeStats.getDataHourTradeStats(
                    lastHourTradeStats, True, tickers)
                lastHourOrderStats: list = getDataOrderStats.getDataHourOrderStats(
                    lastHourOrderStats, True, tickers)

            # if len(lastHourTradeStats) == 0:
            #         lastHourTradeStats = nowTradeStats
            #         lastHourOrderStats = nowOrderStats
            #         #здесб продолжить, нужно добавить корректное время и обрабатывать
            # else: #если данные какие то уже есть за последний час
            #         pass
        else:
            pass

        # ждём 2,5 минуты
        if not flag:
            break
        time.sleep(150)

        # now_day = now_day + datetime.timedelta(days=1)


def start_algo():
    print("I\'m in getDataOnliine")
    print(f'Flag is {flag}')
    tickers = ['SBER', 'GAZP', 'ROSN', 'NVTK', 'GMKN',
               'YNDX', 'LKOH', 'PLZL', 'MOEX', 'PHOR']

    start(tickers, datetime.date(2023, 12, 7))


flag = True
