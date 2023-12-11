from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import threading
import os
import algo_test
# from misc import getDataOnline

users_folder_path = 'Logs'
app = Flask(__name__)
CORS(app)


class GetDataOnline:
    flag = False
    thread = None

    @classmethod
    def start_algo(cls, capital, percent, days):
        # Проверяем, что поток не запущен и флаг установлен
        if cls.thread is None or not cls.thread.is_alive():
            cls.thread = threading.Thread(
                target=cls._algo_thread, args=(capital, percent, days))
            cls.thread.start()

    @classmethod
    def _algo_thread(cls, capital, percent, days):
        algo_test.stop_flag = False
        # getDataOnline.flag = True
        # try:
        algo_test.start_algo(capital, percent, days)
        # getDataOnline.start_algo()
        # except Exception as ex:
        #     print(f"Ended cycle with ex:\n{ex}")

    @classmethod
    def stop_algo(cls):
        cls.flag = False
        algo_test.stop_flag = True
        # getDataOnline.flag = False


getDataOnline_ = GetDataOnline()


def get_all_filenames():
    return sorted([f for f in os.listdir(users_folder_path) if f.endswith('.json')])


def read_and_remove_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    os.remove(file_path)
    return data


@app.route('/register_user', methods=['POST'])
def registration_request():
    '''
    Метод, принимающий POST-запрос. На входе ожидается json, содержащий 
    логин и пароль инвестора.
    '''
    request_ = request.get_json()
    response = jsonify({'Answer': 'successful'})
    with open('user_info/users.json', 'r') as f:
        data = json.load(f)

    if request_["login"] in data:
        return jsonify({"Answer": "Already exists"})
    else:

        data[request_["login"].lower()] = {'password': request_["password"]}
        with open(f'user_info/{request_["login"]}.json', 'w') as f:
            f.write("{}")

    with open('user_info/users.json', 'w') as file:
        json.dump(data, file)

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/<login>/trading', methods=["POST"])
def handle_post_request(login):
    '''
        Метод, принимающий POST-запрос.
        login -- логин пользователя
    '''
    response = jsonify({'Answer': 'successful'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    with open('user_info/users.json', 'r') as f:
        user_json = json.load(f)
        if login not in user_json:
            response = jsonify({'Answer': 'User did not found'})
            return response

    # В <login>.json хранится информация пользователя login.
    # Параметры джсона: сумма на счёте (sum), выбранный алгоритм (algo),
    #                   допустимый процент (percent), количество дней
    with open(f'user_info/{login}.json', 'w') as f:
        request_ = request.get_json()
        json.dump(request_, f)

    return response


@app.route('/<login>/trading/startbot', methods=["POST"])
def startbot(login):
    request_ = request.get_json()
    response = jsonify({'Answer': 'successful'})
    with open('user_info/users.json', 'r') as f:
        user_json = json.load(f)
        if login not in user_json:
            response = jsonify({'Answer': 'User did not found'})
            return response

    with open(f'user_info/{login}.json', 'r') as f:
        usr_info_json = json.load(f)
        capital = int(usr_info_json["fond"])
        percent = int(usr_info_json["percentOfPossibleLoss"])
        days = int(usr_info_json["daysOfTrade"])

    if request_["command"] == "start":
        # print("\nSwitch ON\n")
        # getDataOnline.flag = True
        getDataOnline_.start_algo(capital, percent, days)
    else:
        # print("\nSwitch OFF\n")
        # getDataOnline.flag = False
        getDataOnline_.stop_algo()
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/<login>/trading/stats', methods=["GET"])
def get_stats(login):
    filenames = get_all_filenames()

    print(filenames)

    if filenames:
        all_data = []

        for filename in filenames:
            file_path = os.path.join(users_folder_path, filename)
            data = read_and_remove_file(file_path)
            all_data.extend(data)

        response = jsonify(all_data)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        return jsonify([{"Size of array": len(filenames)}])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
