import os
import ujson
import urequests
import network
import socket
import time
import ustruct
import _thread

def do_connect(essid, password):
    '''
    根据给定的eddid和password连接wifi
    :param essid:  wifi sid
    :param password:  password
    :return:  None
    '''
    if essid == None or essid == '':
        raise BaseException('essid can not be null')
    if password == None or password == '':
        raise BaseException('password can not be null')
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.active():
        print("set sta active")
        sta_if.active(True)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.connect(essid, password)
        retry_times = 30
        while not sta_if.isconnected() and retry_times > 0:
            print(" wait a moment i will try %s items,please" % retry_times)
            time.sleep(2)
            retry_times -= 1
    print('network config:', sta_if.ifconfig())
 


def setmytime():
  while True:
    url = 'http://quan.suning.com/getSysTime.do'
    res=urequests.get(url).text
    #print(res)
    j=ujson.loads(res)
    t2_date = j['sysTime2'].split()[0] #日期
    t2_time = j['sysTime2'].split()[1] #时间
    t_time=t2_date+' '+t2_time
    print (t_time)


    msg={
    "AuthWfpUser":"1",
    "AuthTimeStamp":"2",
    "AuthSign":"3",
    "EquipmentId":"12345678",
    "EquipmentType":"1",
    "AlarmStatus":"1",
    "AlarmTime":"2021-12-14 15:01:12"
    }	
    msg = ujson.dumps(msg)
    response = urequests.post("http://radar.kinsol.net/api/fall/alarm", data = msg)

    print(type(msg))
    #print(type(parsed))
    print(response.text)
    print("success!")
    time.sleep(4)
 
if __name__ == '__main__':

  #连接WiFi
  essid = "iQ"
  password = "123456789"
  do_connect(essid, password)
  #dataunpack()
  #sendcfg()


  #_thread.start_new_thread(setmytime,())
  #t=setmytime()
  #print(t)


  #while True:
    
    #senddata()
    #time.sleep(5)
  #wlan.disconnect()   #断开WiFi
