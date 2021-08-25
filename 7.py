# {"is_success": true, "message": "please visit http://202.207.12.156:9014/context/c03152f5db8918b9905d449686685f77"}

#原来a[][]数组越界了python都不一定管。别等着报错，自己管好他别让他有溢出的可能

import requests
import json
import numpy as np

def anal_cb():
    global cbs
    cbs=''
    f1 = f2 = f3 = f4 = None
    for dot in coord:
        a = ord(dot[0]) - 96 - 1
        b = ord(dot[1]) - 96 - 1

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

        # print('\n')
url ="http://202.207.12.156:9014/step_07"

r = requests.get(url)

js = r.text

dic =json.loads(js)
board = dic["board"]
coord = dic["coord"]

# board= 'HHJHKGIILFHJJFJJKFIFKEKHIGGILD'
# coord =['IG']
global cb
cb = np.full((15,15),'.')
# print(cb)

num = 0

global cbs
cbs=''
for i in range(0,len(board),2):
    a = ord(board[i])-96
    b = ord(board[i+1])- 96
    if num%2==0:
        cb[a-1][b-1] = 'x'
    else:
        cb[a-1][b-1] = 'o'
    num += 1
nn=0
print(cb)

anal_cb()
print(cbs)

params={
    "ans":cbs
}

r = r = requests.get(url,params=params)
print(r.text)

