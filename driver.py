# {"is_success": true, "message": "please visit http://202.207.12.156:9014/context/2e329756827e42330f7897cc9499588e"}

# http://202.207.12.156:9014/game/44160
import time

import requests
import json
import AI

# user_name = "robot"
user_name="0191121332"
black = True

data = ''
k=0

def send_cb(**args):
    url = "http://202.207.12.156:9014/play_game/{game_id}".format(game_id=args['game_id'])
    user = args["user"]
    password = args["password"]
    params = {
        "user": user,
        "password": password,
        "coord": args["coord"],
        "data_type": "json"
    }

    r = requests.get(url, params=params)
    print(r.text)
    dd = r.text
    return dd


def send_login(**args):
    url = "http://202.207.12.156:9014/join_game"
    user = args["user"]
    password = args["password"]
    params = {
        "user": user,
        "password": password,
        "data_type": "json"
    }

    r = requests.get(url, params=params)
    print(r.text)


    dd = r.text
    return dd


def play_game(game_id, board, black):
    user, password = login()
    coord = ''
    coord = AI.excute(board, black)
    print("coord:",coord)

    data = send_cb(game_id=game_id, user=user, password=password, coord=coord)


def join_gg2():
    user = 'alpajo'
    key = "123456"
    password = cryptography(key)
    data = send_login(user=user, password=password)
    r = json.loads(data)
    print('alpajo陪练:','http://202.207.12.156:9014/game/{}'.format(r["game_id"]))
    return r["game_id"]


def join_game():
    user, password = login()
    data = send_login(user=user, password=password)
    r = json.loads(data)
    print('AI:','http://202.207.12.156:9014/game/{}'.format(r["game_id"]))

    return r["game_id"]


def check_game():
    url = "http://202.207.12.156:9014/check_game/{game_id}".format(game_id=game_id)
    r = requests.get(url)
    print(r.text)
    data = json.loads(r.text)
    # print("last_step",data["last_step"])
    return data


def game(game_id):
    global black
    # 判断游戏结束
    import time

    global data
    time.sleep(3)
    data = check_game()

    left_time = int(data["left_time"])
    winner = data["winner"]

    if winner != "None" or left_time == 0:
        # 游戏结束
        print("游戏结束")
        print("winner:", winner)
        print("程序结束")
        exit()
    elif data["ready"]:
        # 准备就绪，可以开始下棋

        # 判断我是黑白棋
        if data["creator_name"] == user_name:
            if data["creator_stone"] == 'x':
                black = True
            else:
                black = False
        else:
            if data["opponent_stone"] == 'x':
                black = True
            else:
                black = False

        if data["current_turn"] == user_name:
            play_game(game_id, data["board"], black)


def login():
    user = user_name
    key = "Wyh20001013"
    return user, cryptography(key)


def cryptography(str1):
    # 加密
    ll = len(str1)
    sum = 0
    for i in range(0, ll):
        sum += ord(str1[ll - i - 1]) * pow(256, i)

    mm = pow(sum, 65537,
             135261828916791946705313569652794581721330948863485438876915508683244111694485850733278569559191167660149469895899348939039437830613284874764820878002628686548956779897196112828969255650312573935871059275664474562666268163936821302832645284397530568872432109324825205567091066297960733513602409443790146687029)

    mm = hex(mm)
    return mm


def main():
    check_game(game_id)


if __name__ == '__main__':
    join_gg2()
    game_id = join_game()

    check_game()
    while 1:
        game(game_id)
