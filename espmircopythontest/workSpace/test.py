import _thread
import utime

import ujson
import urequests



def hello():
  print("hello")

def th_func1():
  while True:
    print('startfanc1')
    utime.sleep(5)

  
def sett():
  print("setttt")
  url = 'http://quan.suning.com/getSysTime.do'
  res=urequests.get(url).text
  print(res)
  j=ujson.loads(res)
  t2_date = j['sysTime2'].split()[0] #日期
  t2_time = j['sysTime2'].split()[1] #时间
  #print(t2_date+' '+t2_time)
  t=t2_date+' '+t2_time
  
  return t
  
def th_func2():

  hello()
  url = 'http://quan.suning.com/getSysTime.do'
  res=urequests.get(url).text
  print(res)
  #t=sett()

  #print(t)
  
 




 

def connectWifi(ssid,passwd):   
  global wlan
  port = 10000  #端口号
  wlan = None  #wlan
  listenSocket = None  #套接字 
  wlan = network.WLAN(network.STA_IF) 
  wlan.active(True)   #激活网络
  wlan.disconnect()   #断开WiFi连接
  wlan.connect(ssid, passwd)   #连接WiFi
  while(wlan.ifconfig()[0] == '0.0.0.0'):   #等待连接
    time.sleep(1)
  ip = wlan.ifconfig()[0]   #获取IP地址
  print(ip)
  return True
  



if __name__ == '__main__':

  #连接WiFi

  SSID = "test"  #修改为你的WiFi名称
  PASSWORD = "henganzhuoyue"  #修改为你WiFi密码

  #Catch exceptions,stop program if interrupted accidentally in the 'try'
  connectWifi(SSID,PASSWORD)
  url = 'http://quan.suning.com/getSysTime.do'
  res=urequests.get(url).text
  print(res)

  #_thread.start_new_thread(th_func2,())
  #th_func2()
  
  wlan.disconnect()

