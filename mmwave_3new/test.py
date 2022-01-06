import requests
import json

a={"0":"1","2":"4"}
b={"0":"4"}
url = 'https://apps.game.qq.com/CommArticle/app/reg/gdate.php'
url2 = 'http://quan.suning.com/getSysTime.do'
url3='http://api.k780.com/?app=time.world&city_en=new-york&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json'
tempdict={1:(2,3,4,5,6,7),2:(3,2,5,6,7,0)}
tempdict1={1:(2,3,4,5,6,7)}
tt=[{0: (0.43, 0.34, 0.145, 0.0, 0.0, 0)}, {0: (0.43, 0.34, 0.145, 0.0, 0.0, 0)}, {0: (0.43, 0.34, 0.145, 0.0, 0.0, 0)}, {0: (0.43, 0.34, 0.145, 0.0, 0.0, 0)}, {0: (0.43, 0.34, 0.145, 0.0, 0.0, 0)}, None, None, None, None, None, None, None, None, None, None]
c=[]
e={1:(2,3,4,5,6,7)}

print(e)
# if e:
#     print("......")
# with open("test.log","a") as f:
#     f.write("error!")
#     f.write("\n")
qqq=requests.get(url).text
print(qqq[20:-2])



r=requests.get(url2)
pp=r.json()
print(pp["sysTime2"])


# res=requests.get(url3)
# aa=res.json()
#
# print(aa["result"]["bjt_datetime"])



