import warnings

# Отключаем предупреждения от sklearn
warnings.filterwarnings(action='ignore')

import pandas as pd
import numpy as np
from moexalgo import Ticker
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
import joblib
import time
import json
import os
import gdown
import patoolib
import os

destination_folder = '.'
if not os.path.join(destination_folder, 'Weights'):
    file_id = '1JSRVPGzLyjkcHvvYNNRxOODUOXPr9fnY'
    url = f'https://drive.google.com/uc?id={file_id}'

    output_file = os.path.join(destination_folder, 'archive.rar')
    gdown.download(url, output_file, quiet=False)

    patoolib.extract_archive(output_file, outdir=destination_folder)

    os.remove(output_file)



def define_trend(end_date):
    TREND_ANGLE = 30
    top_5_tickers = ['SBER', 'ROSN', 'NVTK', 'GMKN', 'YNDX', 'LKOH', 'PLZL', 'MOEX', 'PHOR', 'GAZP']

    period = 'D'

    end_date = end_date

    start_date = end_date - timedelta(days=7)

    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    trend_analysis_results = {}

    for ticker in top_5_tickers:

        current_ticker = Ticker(ticker)
        candles = current_ticker.candles(date=start_date_str, till_date=end_date_str, period=period)
        candles = pd.DataFrame(candles)
        x = np.arange(len(candles))  
        y = list(candles['close'])

        slope, _ = np.polyfit(x, y, 1)

        angle_rad = np.arctan2(y[-1] - y[0], x[-1] - x[0])

        angle_deg = np.degrees(angle_rad)

        trend = 'Up' if (slope > 0 and angle_deg >= TREND_ANGLE) else 'Down' if (slope < 0 and angle_deg < -TREND_ANGLE) else 'Flat'

        is_continue = (trend == 'Up' or trend == 'Down')

        trend_analysis_results[ticker] = is_continue

    return (trend_analysis_results)

def prepare_data(data):
    
    data_c = data.copy()
    # Рассчитываем разницу между ценой открытия и ценой закрытия
    data_c['pr_diff'] = data_c['pr_close'] - data_c['pr_open']

    # Удаляем колонки 'pr_open' и 'pr_close'
    data_c.drop(['pr_open', 'pr_close'], axis=1, inplace=True)

    # Рассчитываем разницу между 'pr_high' и 'pr_low' со знаком значения 'pr_diff'
    data_c['pr_lh_diff'] = data_c['pr_high'] - data_c['pr_low']
    data_c['pr_lh_diff'] *= data_c['pr_diff'].apply(lambda x: 1 if x >= 0 else -1)

    # Удаляем колонки 'pr_high' и 'pr_low'
    data_c.drop(['pr_high', 'pr_low'], axis=1, inplace=True)

    data_c = data_c.drop(columns=['tradedate', 'tradetime', 'secid', 'pr_vwap_s', 'put_vwap_b', 'put_vwap_s', 'cancel_vwap_s', 'cancel_vwap_b', 'pr_std', 'pr_vwap_b'])

    return data_c


# trend_tickers = define_trend(datetime.strptime('2020-01-10', '%Y-%m-%d'))
# long_trend_tickers = [i for i in trend_tickers if trend_tickers[i]]

sber_model = joblib.load('Weights/sber_random_forest_model_not_pipeline.joblib')
rosn_model = joblib.load('Weights/rosn_random_forest_model_not_pipeline.joblib')
nvtk_model = joblib.load('Weights/nvtk_random_forest_model_not_pipeline.joblib')
gmkn_model = joblib.load('Weights/gmkn_random_forest_model_not_pipeline.joblib')
yndx_model = joblib.load('Weights/yndx_random_forest_model_not_pipeline.joblib')
lkoh_model = joblib.load('Weights/lkoh_random_forest_model_not_pipeline.joblib')
plzl_model = joblib.load('Weights/plzl_random_forest_model_not_pipeline.joblib')
moex_model = joblib.load('Weights/moex_random_forest_model_not_pipeline.joblib')
phor_model = joblib.load('Weights/phor_random_forest_model_not_pipeline.joblib')
gazp_model = joblib.load('Weights/gazp_random_forest_model_not_pipeline.joblib')

models_dict = {'SBER': sber_model, 'ROSN': rosn_model, 'NVTK': nvtk_model, 'GMKN': gmkn_model, 'YNDX': yndx_model, 'LKOH': lkoh_model, 'PLZL': plzl_model, 'MOEX': moex_model, 'PHOR': phor_model, 'GAZP': gazp_model}
# long_trend_models = [models_dict[i] for i in long_trend_tickers]

sber_test_df = pd.read_csv('Test_data/SBER_test.csv')
rosn_test_df = pd.read_csv('Test_data/ROSN_test.csv')
nvtk_test_df = pd.read_csv('Test_data/NVTK_test.csv')
gmkn_test_df = pd.read_csv('Test_data/GMKN_test.csv')
yndx_test_df = pd.read_csv('Test_data/YNDX_test.csv')
lkoh_test_df = pd.read_csv('Test_data/LKOH_test.csv')
plzl_test_df = pd.read_csv('Test_data/PLZL_test.csv')
moex_test_df = pd.read_csv('Test_data/MOEX_test.csv')
phor_test_df = pd.read_csv('Test_data/PHOR_test.csv')
gazp_test_df = pd.read_csv('Test_data/GAZP_test.csv')

test_df_dict = {'SBER': sber_test_df, 'ROSN': rosn_test_df, 'NVTK': nvtk_test_df, 'GMKN': gmkn_test_df, 'YNDX': yndx_test_df, 'LKOH': lkoh_test_df, 'PLZL': plzl_test_df, 'MOEX': moex_test_df, 'PHOR': phor_test_df, 'GAZP': gazp_test_df}

# trend_test_df = [test_df_dict[i] for i in long_trend_tickers]


sber_prepared_for_model_df = prepare_data(sber_test_df)
rosn_prepared_for_model_df = prepare_data(rosn_test_df)
nvtk_prepared_for_model_df = prepare_data(nvtk_test_df)
gmkn_prepared_for_model_df = prepare_data(gmkn_test_df)
yndx_prepared_for_model_df = prepare_data(yndx_test_df)
lkoh_prepared_for_model_df = prepare_data(lkoh_test_df)
plzl_prepared_for_model_df = prepare_data(plzl_test_df)
moex_prepared_for_model_df = prepare_data(moex_test_df)
phor_prepared_for_model_df = prepare_data(phor_test_df)
gazp_prepared_for_model_df = prepare_data(gazp_test_df)

sber_prepared_for_model_df .drop(columns=['target'], inplace=True)
rosn_prepared_for_model_df .drop(columns=['target'], inplace=True)
nvtk_prepared_for_model_df .drop(columns=['target'], inplace=True)
gmkn_prepared_for_model_df .drop(columns=['target'], inplace=True)
yndx_prepared_for_model_df .drop(columns=['target'], inplace=True)
lkoh_prepared_for_model_df .drop(columns=['target'], inplace=True)
plzl_prepared_for_model_df .drop(columns=['target'], inplace=True)
moex_prepared_for_model_df .drop(columns=['target'], inplace=True)
phor_prepared_for_model_df .drop(columns=['target'], inplace=True)
gazp_prepared_for_model_df .drop(columns=['target'], inplace=True)

prepared_df_dict = {'SBER': sber_prepared_for_model_df, 'ROSN': rosn_prepared_for_model_df, 'NVTK': nvtk_prepared_for_model_df, 'GMKN': gmkn_prepared_for_model_df, 'YNDX': yndx_prepared_for_model_df, 'LKOH': lkoh_prepared_for_model_df, 'PLZL': plzl_prepared_for_model_df, 'MOEX': moex_prepared_for_model_df, 'PHOR': phor_prepared_for_model_df, 'GAZP': gazp_prepared_for_model_df}
# prepared_df = [prepared_df_dict[i] for i in long_trend_tickers]

def find_trend_models(long_trend_tickers, models_dict):
    long_trend_models = [models_dict[i] for i in long_trend_tickers]
    return long_trend_models

def find_trend_test_dfs(long_trend_tickers, test_df_dict):
    trend_test_df = [test_df_dict[i] for i in long_trend_tickers]
    return trend_test_df

def find_trend_prepared_dfs(long_trend_tickers, prepared_df_dict):
    prepared_df = [prepared_df_dict[i] for i in long_trend_tickers]
    return prepared_df

stop_flag = False

def ml_trade_algorithm(capital, loss_percent=None, trade_days=None):
    global stop_flag
    today = datetime.strptime('2020-01-10', '%Y-%m-%d').date()
    current_capital = capital * 1000
    stop_loss = 0.005
    take_profit = 1.01
    actives = []

    for _ in range(trade_days):

        if stop_flag:
            print("Algorithm stopped by user.")
            break  
        
        trend_tickers = define_trend(today)
        long_trend_tickers = [i for i in trend_tickers if trend_tickers[i]]
        models = find_trend_models(long_trend_tickers, models_dict)
        capital_per_model = current_capital / 3

        test_dfs = find_trend_test_dfs(long_trend_tickers, test_df_dict)
        prepared_dfs = find_trend_prepared_dfs(long_trend_tickers, prepared_df_dict)

        for j in range(len(models)):
            model = models[j]
            test_df = test_dfs[j]
            iter_test_df = test_df[test_df['tradedate'] == str(today)]
            prepared_df = prepared_dfs[j]

            if not iter_test_df.empty:
                first_row = iter_test_df.iloc[0]
                prev_row = first_row

            for index, row in iter_test_df.iterrows():
    
                for active in actives:
                    at = datetime.strptime(active['time'], '%H:%M:%S').time()
                    pt = datetime.strptime(prev_row['tradetime'], '%H:%M:%S').time()

                    if at == pt:
                        if row['pr_low'] <= active['price']*(1-stop_loss):
                            current_capital += active['price']*(1-stop_loss)*active['amount']
                            name = active['name']
                            sell_count = active['amount']
                            sell_price = active['price']*(1-stop_loss)
                            action = 'sell'
                            sell_date = row['tradedate']
                            sell_time = row['tradetime']
                            combined_datetime_str = f'{sell_date}T{sell_time}'
                            combined_datetime = datetime.strptime(combined_datetime_str, '%Y-%m-%dT%H:%M:%S')
                            actives.remove(active)
                            file_number = get_next_file_number('Logs')
                            file_path = f'Logs/{file_number}_transaction.json'

                            try:    
                                with open(file_path, 'r') as file:
                                    transactions = json.load(file)
                            except FileNotFoundError:
                                transactions = []

                            transaction_data = {
                                'name': name,
                                'amount': sell_count,
                                'price': sell_price,
                                'action': action,
                                'date': combined_datetime.isoformat(),
                                'balance': current_capital
                            }
                            transactions.append(transaction_data)

                            with open(file_path, 'w') as file:
                                json.dump(transactions, file, indent=2)

                            print(f"Продажа успешно добавлена в файл {file_path}")
                            
                        elif row['pr_high'] >= active['price']*take_profit:
                            current_capital += active['price']*take_profit*active['amount']
                            name = active['name']
                            sell_count = active['amount']
                            sell_price = active['price']*take_profit
                            action = 'sell'
                            sell_date = row['tradedate']
                            sell_time = row['tradetime']
                            combined_datetime_str = f'{sell_date}T{sell_time}'
                            combined_datetime = datetime.strptime(combined_datetime_str, '%Y-%m-%dT%H:%M:%S')
                            actives.remove(active)
                            file_number = get_next_file_number('Logs')
                            file_path = f'Logs/{file_number}_transaction.json'

                            try:    
                                with open(file_path, 'r') as file:
                                    transactions = json.load(file)
                            except FileNotFoundError:
                                transactions = []

                            transaction_data = {
                                'name': name,
                                'amount': sell_count,
                                'price': sell_price,
                                'action': action,
                                'date': combined_datetime.isoformat(),
                                'balance': current_capital
                            }
                            transactions.append(transaction_data)

                            with open(file_path, 'w') as file:
                                json.dump(transactions, file, indent=2)

                            print(f"Продажа успешно добавлена в файл {file_path}")

                        else:
                            current_capital += active['amount']*row['pr_close']
                            name = active['name']
                            sell_count = active['amount']
                            sell_price = row['pr_close']
                            action = 'sell'
                            sell_date = row['tradedate']
                            sell_time = row['tradetime']
                            combined_datetime_str = f'{sell_date}T{sell_time}'
                            combined_datetime = datetime.strptime(combined_datetime_str, '%Y-%m-%dT%H:%M:%S')
                            actives.remove(active)
                            file_number = get_next_file_number('Logs')
                            file_path = f'Logs/{file_number}_transaction.json'

                            try:    
                                with open(file_path, 'r') as file:
                                    transactions = json.load(file)
                            except FileNotFoundError:
                                transactions = []

                            transaction_data = {
                                'name': name,
                                'amount': sell_count,
                                'price': sell_price,
                                'action': action,
                                'date': combined_datetime.isoformat(),
                                'balance': current_capital
                            }
                            transactions.append(transaction_data)

                            with open(file_path, 'w') as file:
                                json.dump(transactions, file, indent=2)

                            print(f"Продажа успешно добавлена в файл {file_path}")
                prev_row = row
                pred = model.predict(prepared_df.iloc[index].values.reshape(1, -1))
                if pred[0] == 1:
                    buy_count = capital_per_model // row['pr_close']
                    duy_date = row['tradedate']
                    buy_time = row['tradetime']
                    combined_datetime_str = f'{duy_date}T{buy_time}'
                    combined_datetime = datetime.strptime(combined_datetime_str, '%Y-%m-%dT%H:%M:%S')
                    buy_price = row['pr_close']
                    name = row['secid']  
                    action = 'buy'
                    
                    if current_capital - buy_count*buy_price >= 0:
                        file_number = get_next_file_number('Logs')
                        file_path = f'Logs/{file_number}_transaction.json'
                        current_capital -= buy_count*buy_price
                        try:    
                            with open(file_path, 'r') as file:
                                transactions = json.load(file)
                        except FileNotFoundError:
                            transactions = []

                        transaction_data = {
                            'name': name,
                            'amount': buy_count,
                            'price': buy_price,
                            'action': action,
                            'date': combined_datetime.isoformat(),
                            'balance': current_capital
                        }
                        transactions.append(transaction_data)

                        with open(file_path, 'w') as file:
                            json.dump(transactions, file, indent=2)

                        print(f"Покупка успешно добавлена в файл {file_path}")

                        actives.append({'name': name, 'amount': buy_count, 'time': buy_time, 'date': duy_date ,'price': buy_price})
        today = today + timedelta(days=1)

def get_next_file_number(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return 1
    
    existing_files = [f for f in os.listdir(folder_path) if f.endswith(".json") and '_' in f]
    
    if not existing_files:
        return 1
    
    existing_numbers = [int(f.split("_")[0]) for f in existing_files]
    
    next_number = max(existing_numbers) + 1
    
    return next_number


if __name__ == "__main__":
    ml_trade_algorithm(100, trade_days=7)