import driver

GRID_WIDTH = 40

COLUMN = 15
ROW = 15

user_name = '0191121332'
my_password = "Wyh20001013"

list1 = []  # AI Me
list2 = []  # human oppnent
list3 = []  # 棋盘上有子的位置all

list_all = []  # 整个棋盘的点
next_point = [0, 0]  # AI下一步最应该下的位置

ratio = 1  # 进攻的系数   大于1 进攻型，  小于1 防守型
DEPTH = 3  # 搜索深度   只能是单数。  如果是负数， 评估函数评估的的是自己多少步之后的自己得分的最大值，并不意味着是最好的棋， 评估函数的问题

# 棋型的评估分数
shape_score = [(50, (0, 1, 1, 0, 0)),
               (50, (0, 0, 1, 1, 0)),
               (200, (1, 1, 0, 1, 0)),
               (500, (0, 0, 1, 1, 1)),
               (500, (1, 1, 1, 0, 0)),
               (5000, (0, 1, 1, 1, 0)),
               (5000, (0, 1, 0, 1, 1, 0)),
               (5000, (0, 1, 1, 0, 1, 0)),
               (5000, (1, 1, 1, 0, 1)),
               (5000, (1, 1, 0, 1, 1)),
               (5000, (1, 0, 1, 1, 1)),
               (5000, (1, 1, 1, 1, 0)),
               (5000, (0, 1, 1, 1, 1)),
               (50000, (0, 1, 1, 1, 1, 0)),
               (99999999, (1, 1, 1, 1, 1))]


# 得到落点位置
def ai(black):
    global cut_count  # 统计剪枝次数
    cut_count = 0
    global search_count  # 统计搜索次数
    search_count = 0
    negamax(True, DEPTH, -99999999, 99999999)
    print("本次共剪枝次数：" + str(cut_count))
    print("本次共搜索次数：" + str(search_count))
    return next_point[0], next_point[1]


# 负值极大算法搜索 alpha + beta剪枝
def negamax(is_ai, depth, alpha, beta):
    # 游戏是否结束 | | 探索的递归深度是否到边界
    if game_win(list1) or game_win(list2) or depth == 0:
        return evaluation(is_ai)

    blank_list = list(set(list_all).difference(set(list3)))
    order(blank_list)  # 搜索顺序排序  提高剪枝效率 将上一步落子位置最临近的点放到列表最前面
    # 遍历每一个候选步
    for next_step in blank_list:

        global search_count
        search_count += 1

        # 如果要评估的位置没有相邻的子， 则不去评估  减少计算
        if not has_neightnor(next_step):
            continue

        if is_ai:
            list1.append(next_step)
        else:
            list2.append(next_step)
        list3.append(next_step)

        value = -negamax(not is_ai, depth - 1, -beta, -alpha)
        if is_ai:
            list1.remove(next_step)
        else:
            list2.remove(next_step)
        list3.remove(next_step)

        if value > alpha:

            print(str(value) + "alpha:" + str(alpha) + "beta:" + str(beta))
            print(list3)
            if depth == DEPTH:
                next_point[0] = next_step[0]
                next_point[1] = next_step[1]
            # alpha + beta剪枝点
            if value >= beta:
                global cut_count
                cut_count += 1
                return beta
            alpha = value

    return alpha


#  离最后落子的邻居位置最有可能是最优点
def order(blank_list):
    last_pt = list3[-1]
    for item in blank_list:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if (last_pt[0] + i, last_pt[1] + j) in blank_list:
                    blank_list.remove((last_pt[0] + i, last_pt[1] + j))
                    blank_list.insert(0, (last_pt[0] + i, last_pt[1] + j))


def has_neightnor(pt):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if (pt[0] + i, pt[1] + j) in list3:
                return True
    return False


# 评估函数
def evaluation(is_ai):
    total_score = 0

    if is_ai:
        my_list = list1
        enemy_list = list2
    else:
        my_list = list2
        enemy_list = list1

    # 算自己的得分
    score_all_arr = []  # 得分形状的位置 用于计算如果有相交 得分翻倍
    my_score = 0
    for pt in my_list:
        m = pt[0]
        n = pt[1]
        my_score += cal_score(m, n, 0, 1, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, 1, 0, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, 1, 1, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, -1, 1, enemy_list, my_list, score_all_arr)

    #  算敌人的得分， 并减去
    score_all_arr_enemy = []
    enemy_score = 0
    for pt in enemy_list:
        m = pt[0]
        n = pt[1]
        enemy_score += cal_score(m, n, 0, 1, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, 1, 0, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, 1, 1, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, -1, 1, my_list, enemy_list, score_all_arr_enemy)

    total_score = my_score - enemy_score * ratio * 0.1

    return total_score


# 每个方向上的分值计算
def cal_score(m, n, x_decrict, y_derice, enemy_list, my_list, score_all_arr):
    add_score = 0  # 加分项
    # 在一个方向上， 只取最大的得分项
    max_score_shape = (0, None)

    # 如果此方向上，该点已经有得分形状，不重复计算
    for item in score_all_arr:
        for pt in item[1]:
            if m == pt[0] and n == pt[1] and x_decrict == item[2][0] and y_derice == item[2][1]:
                return 0

    # 在落子点 左右方向上循环查找得分形状
    for offset in range(-5, 1):
        # offset = -2
        pos = []
        for i in range(0, 6):
            if (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in enemy_list:
                pos.append(2)
            elif (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in my_list:
                pos.append(1)
            else:
                pos.append(0)
        tmp_shap5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
        tmp_shap6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])

        for (score, shape) in shape_score:
            if tmp_shap5 == shape or tmp_shap6 == shape:
                if tmp_shap5 == (1, 1, 1, 1, 1):
                    print('wwwwwwwwwwwwwwwwwwwwwwwwwww')
                if score > max_score_shape[0]:
                    max_score_shape = (score, ((m + (0 + offset) * x_decrict, n + (0 + offset) * y_derice),
                                               (m + (1 + offset) * x_decrict, n + (1 + offset) * y_derice),
                                               (m + (2 + offset) * x_decrict, n + (2 + offset) * y_derice),
                                               (m + (3 + offset) * x_decrict, n + (3 + offset) * y_derice),
                                               (m + (4 + offset) * x_decrict, n + (4 + offset) * y_derice)),
                                       (x_decrict, y_derice))

    # 计算两个形状相交， 如两个3活 相交， 得分增加 一个子的除外
    if max_score_shape[1] is not None:
        for item in score_all_arr:
            for pt1 in item[1]:
                for pt2 in max_score_shape[1]:
                    if pt1 == pt2 and max_score_shape[0] > 10 and item[0] > 10:
                        add_score += item[0] + max_score_shape[0]

        score_all_arr.append(max_score_shape)

    return add_score + max_score_shape[0]


def game_win(list):
    for m in range(COLUMN):
        for n in range(ROW):

            if n < ROW - 4 and (m, n) in list and (m, n + 1) in list and (m, n + 2) in list and (
                    m, n + 3) in list and (m, n + 4) in list:
                return True
            elif m < ROW - 4 and (m, n) in list and (m + 1, n) in list and (m + 2, n) in list and (
                    m + 3, n) in list and (m + 4, n) in list:
                return True
            elif m < ROW - 4 and n < ROW - 4 and (m, n) in list and (m + 1, n + 1) in list and (
                    m + 2, n + 2) in list and (m + 3, n + 3) in list and (m + 4, n + 4) in list:
                return True
            elif m < ROW - 4 and n > 3 and (m, n) in list and (m + 1, n - 1) in list and (
                    m + 2, n - 2) in list and (m + 3, n - 3) in list and (m + 4, n - 4) in list:
                return True
    return False


# 密码加密
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


# 向服务器发送落子位置
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
    import requests
    r = requests.get(url, params=params)
    print(r.text)
    dd = r.text
    return dd


# 登录
def login():
    user = user_name
    key = my_password
    return user, cryptography(key)


# 转换为要求坐标格式
def transfer_abc(pos):
    a = chr(pos[0] + 97)
    b = chr(pos[1] + 97)
    print(b + a)
    return b + a


# 出棋
def play_game(game_id, pos):
    user, password = login()
    sss = transfer_abc(pos)
    data = send_cb(game_id=game_id, user=user, password=password, coord=pos)


def main():
    for i in range(COLUMN):
        for j in range(ROW):
            list_all.append((i, j))
    game_id = driver.join_game()
    driver.check_game()
    while 1:
        import time
        time.sleep(3)
        message = driver.check_game()

        left_time = int(message["left_time"])
        winner = message["winner"]

        if winner != "None" or left_time == 0:
            # 游戏结束
            print("游戏结束")
            print("winner:", winner)
            print("程序结束")
            exit()
        elif message["ready"]:
            # 准备就绪，可以开始下棋
            if message["current_turn"] == user_name:
                pos = ai()  # 得出坐标
                play_game(game_id, pos)
                list1.append(pos)
                list3.append(pos)


main()
