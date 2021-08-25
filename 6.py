# Hi 0191121332, please visit http://202.207.12.156:9014/context/3ff280105813f582c7c38dabedd901bc fill text

import requests
import json
import numpy as np
url ="http://202.207.12.156:9014/step_06"

r = requests.get(url)

q = r.text

q = json.loads(q)
# q = eval(q)
# print(q)
# print((type(q)))

n = q["questions"]
print(n)
cb = np.full((15,15),".")

a=0
b=0
nn=0
ss = ''
cbs=''
for i in range(0,len(n),2):
    a = ord(n[i])-96
    b = ord(n[i+1])-96
    print(n[i],ord(n[i]),a)
    if nn%2==0:
        cb[a-1][b-1]='x'
    else:
        cb[a-1][b-1]='o'
    nn+=1
    if i != 0:
        cbs += ','
    for i in range(0,15):
        for j in range(0,15):
            cbs += cb[i][j]


params ={
    "ans":cbs
}

url="http://202.207.12.156:9014/step_06"

r =requests.get(url,params=params)

print(r.url)
print(r.text)
