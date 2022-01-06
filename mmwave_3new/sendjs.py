import serial
import time
import requests

import requests
import json


# -*- coding:utf-8 -*-
#带参数的get


import json

url = "http://radar.kinsol.net/api/handle?equipmentId=12345678"
url="http://radar.kinsol.net/api/handle"
params = {
"equipmentId":"12345678",
}
r = requests.get(url=url,params=params)
print(r.text)


def sendheartbeat():
    hburl = "http://radar.kinsol.net/api/heartbeat"

    while True:
        url = 'http://quan.suning.com/getSysTime.do'
        res = requests.get(url).text
        # print(res)
        j = json.loads(res)
        t2_date = j['sysTime2'].split()[0]  # 日期
        t2_time = j['sysTime2'].split()[1]  # 时间
        time = t2_date + ' ' + t2_time
        msg = {
            "AuthWfpUser": "3",
            "AuthTimeStamp": "2",
            "AuthSign": "1",
            "EquipmentId": "12345678",
            "EquipmentType": "1",
            "EquipmentStatus": "1",
            "peoplecounting": "1",
            "CreationTime": time
        }

        # with open("heatbeat.log", "a") as f:
        # f.write(str(msg))
        # f.write("\n")
        js = json.dumps(msg)

        response = requests.post(hburl, data=js)
        print(msg)
        rescode = response.text
        rescode = rescode[8:11]
        if rescode == "200":

            print("发送心跳成功！")
        else:
            print("发送未成功！")

            # break

        time.sleep(5)
# if __name__ == '__main__':
#     data = {
#         'equipmentId':"12345678",
#         'AlarmStatus': '0'
#     }
#     r = requests.get("http://radar.kinsol.net/api/handle?equipmentId=12345678", params=data)
#     print(r.text)
