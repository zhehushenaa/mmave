import os
import ujson
import urequests
import network
import socket
import time
import ustruct
from pyb import UART




def setmytime():
  url = 'http://quan.suning.com/getSysTime.do'
  res=urequests.get(url).text
  #print(res)
  j=ujson.loads(res)
  t2_date = j['sysTime2'].split()[0] #日期
  t2_time = j['sysTime2'].split()[1] #时间
  t_time=t2_date+' '+t2_time
  return t_time


#def sendcfg():
  
  #u1 = UART(0, 115200) 
  #with open('ISK_6m_default.cfg','r') as f:
    #print(f.readline())
    #u1.write('xianyu')      #发送字符串“xianyu”

print ("stt")

