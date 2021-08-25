
# http://202.207.12.156:9014/context/f64710b4861e6ff10678036548bf7afa
import requests
import json
import math

def mod_css(a,b,c):
    num = str(bin(b))
    k = 1

    sum =[]
    while k<=len(num)-2:
        if num[len(num)-k]=='1':
           sum.append(2**(k-1))
        k+=1
    return sum
url="http://202.207.12.156:9014/step_04"


r = requests.get(url)
q = json.loads(r.text)
str1 = q["questions"]

li = eval(str1)
# print(li)
# str = str.replace('[','',1)
#
# str = str[:-1]
# print(type(li))
# print(li)
# print(li[0])
# print(li[0][0])
result = []
for i in range(0,10):
    a = li[i][0]
    b = li[i][1]
    c = li[i][2]
    # sum = mod_css(a,b,c)
    # x = 1
    # for i in sum:
    #     y = (a**i)%c
    #     x *= y
    # r = x%c
    # r = math.pow(a,b)
    result.append(pow(a,b,c))


jsonre = json.dumps(result)
print(jsonre)

js = jsonre.replace('[','')

js = js.replace(']','')
print(js)

params = {
    "ans":js
}

rp = requests.get(url,params=params)
print(rp.text)


