# {"is_success": true, "message": "please visit http://202.207.12.156:9014/context/701672826a45d8d2d998b3a3f66166bf"}
import requests
import json

import requests
import json
import numpy as np

cbs = ''
cb = np.full((15, 15), '.')
black = True
coord = []
all_score = []
rules = [
    ["CMMMM", "MCMMM", "MMCMM", "MMMCM", "MMMMC"],
    ["OOOOC", "COOOO"],
    [".CMMM.", ".MCMM.", ".MMCM.", ".MMMC."],
    ["COOO.", ".OOOC", ".OOCO.", ".OCOO."],
    ["OCMMM.", "OMCMM.", "OMMCM.", "OMMMC.", ".CMMMO", ".MCMMO", ".MMCMO", ".MMMCO"],
    [".MMC.", ".MCM.", ".CMM."],
    [".OOC", "COO.", "MOOOC", "COOOM"],
    [".MMCO", ".MCMO", ".CMMO", "OMMC.", "OMCM.", "OCMM.", "MOOC", "COOM"],
    [".MC.", ".CM."]
]


def differ_balck(epoch):
    global black
    ll = len(epoch)
    if ll % 2 == 0:
        # 我是黑棋
        black = True
    else:
        black = False


def make_cb(epoch):
    # 落子
    global cb, black
    cb = np.full((15, 15), '.')
    # print(cb)
    num = 0
    # 区分敌我棋子
    if black == True:
        hei = 'M'
        bai = 'O'
    else:
        hei = 'O'
        bai = 'M'
    # 制作棋局
    for i in range(0, len(epoch), 2):
        a = ord(epoch[i]) - 96
        b = ord(epoch[i + 1]) - 96
        if num % 2 == 0:
            cb[a - 1][b - 1] = hei
        else:
            cb[a - 1][b - 1] = bai
        num += 1
    # print(cb)


def cal_cb(a, b):
    global cb, cbs
    f1 = f2 = f3 = f4 = None
    cb[a][b] = 'C'
    # 水平
    for i in range(1, 5):
        if 0 <= b - 5 + i <= 14:
            # print(cb[a-5+i][b],end="")
            cbs += cb[a][b - 5 + i]
            f1 = True
    cbs += cb[a, b]
    for i in range(1, 5):
        if b + i <= 14:
            # print(cb[a+i][b],end="")
            cbs += cb[a][b + i]
            f1 = True
    if f1:
        cbs += ','
    # 左斜
    for i in range(1, 5):
        if 0 <= a - 5 + i <= 14 and 0 <= b - 5 + i <= 14:
            # print(cb[a-5+i][b-5+i],end="")
            cbs += cb[a - 5 + i][b - 5 + i]
            f2 = True

    cbs += cb[a, b]
    for i in range(1, 5):
        if a + i <= 14 and b + i <= 14:
            # print(cb[a+i][b-i],end="")
            cbs += cb[a + i][b + i]
            f2 = True
    if f2:
        cbs += ','

    # 竖直
    for i in range(1, 5):
        if 0 <= a + 5 - i <= 14:
            # print(cb[a][b-5+i],end="")
            cbs += cb[a + 5 - i][b]
            f3 = True

    cbs += cb[a, b]

    for i in range(1, 5):
        if a - i >= 0:
            # print(cb[a][b+i],end="")
            cbs += cb[a - i][b]
            f3 = True
    if f3:
        cbs += ','

    # 右下
    for i in range(1, 5):
        if 0 <= a - 5 + i <= 14 and 0 <= b + 5 - i <= 14:
            # print(cb[a-5+i][b-5+i],end="")
            cbs += cb[a - 5 + i][b + 5 - i]
            f4 = True
    cbs += cb[a, b]

    for i in range(1, 5):
        if a + i <= 14 and b - i >= 0:
            # print(cb[a -i][b - i],end="")
            cbs += cb[a + i][b - i]
            f4 = True

    if (b != 0 and f4):
        cbs += ','
    cb[a][b] = '.'


def analyse_cb():
    # 找空的位置(统计考察点)
    global cb, cbs, coord, all_score
    for i in range(0, 15):
        for j in range(0, 15):
            if cb[i][j] == '.':
                coord.append([i, j])

    # print('coord:', coord)
    # 统计棋型串
    for dot in coord:
        a = dot[0]
        b = dot[1]
        global cbs
        cbs = ''
        cal_cb(a, b)
        match_cb(a, b)
    # 所有的位置分数统计完成,选出最大的分数对应的位置

    # 问题;[[100,1,2],[2000,2,2]]如何比较100和200，取出最大的数？
    max1 = -1
    for sc, a, b in all_score:
        if (sc > max1):
            max1 = sc
            x = a
            y = b
    return max1, x, y


def match_rule(str1):
    scores = [10000, 6000, 5000, 2500, 2000, 400, 400, 200, 50]
    global all_score
    nn = 0
    for rule in rules:


        # 问题出在我们的字符串太全，而规则字符串更精细，要改成我们的字符串里去找规则字符串
        for r in rule:
            if str1.find(r) != -1:
                return scores[nn]
        nn += 1
    return 20


def match_cb(a, b):
    li = cbs.split(',')
    sum = 0
    global all_score
    for str1 in li:
        # 匹配规则并计算该位置的所有棋型字符串的分数
        # print(str1)
        scoree = match_rule(str1)
        sum += scoree
    all_score.append([sum, a, b])


# 取数据
def load_data():
    url = "http://202.207.12.156:9014/step_08"
    r = requests.get(url)
    js = r.text
    dic = json.loads(js)

    q = dic["questions"]
    # print(q)
    return q


def send_data(msg):
    url = "http://202.207.12.156:9014/step_08"
    params = {
        "ans": msg
    }

    r = requests.get(url, params=params)
    print(r.text)


def transfer_abc(x, y):
    a = chr(x + 97)
    b = chr(y + 97)
    print(a + b)
    return a + b


# 开始任务
max_scores = []
if __name__ == '__main__':
    q = load_data()
    for epoch in q:
        all_score = []
        cbs = ''
        cb = np.full((15, 15), '.')
        coord = []
        # 分黑白
        differ_balck(epoch)
        # 做棋盘
        make_cb(epoch)
        # 分析棋型,找出最大分数位置
        max_score, x, y = analyse_cb()
        sss = transfer_abc(x, y)
        max_scores.append(sss)
    jslist = ','.join(max_scores)
    print("jsli", jslist)
    send_data(jslist)