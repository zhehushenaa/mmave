import os
import ujson
import urequests
import network
import socket
import utime
import time
import ustruct
import _thread
from machine import UART,Pin
def do_connect():
  essid = "test"
  password = "henganzhuoyue"
  if essid == None or essid == '':
      raise BaseException('essid can not be null')
  if password == None or password == '':
      raise BaseException('password can not be null')
  sta_if = network.WLAN(network.STA_IF)
  if not sta_if.active():
      print("set sta active")
      sta_if.active(True)
  if sta_if.isconnected():
      sta_if.disconnect()
      print('connecting to network...')
      sta_if.connect(essid, password)
      retry_times = 30
      while not sta_if.isconnected() and retry_times > 0:
          print(" wait a moment i will try %s items,please" % retry_times)
          time.sleep(2)
          retry_times -= 1
  if not sta_if.isconnected():
      print('connecting to network...')
      sta_if.connect(essid, password)
      retry_times = 30
      while not sta_if.isconnected() and retry_times > 0:
          print(" wait a moment i will try %s items,please" % retry_times)
          time.sleep(2)
          retry_times -= 1
  print(sta_if.isconnected())
  print('network config:', sta_if.ifconfig())
  
def hu():
    print("meiiihi")
def shen():
    hu()
    print("shen")
  
if __name__ == '__main__':
  #连接WiFi

  #tlvHeaderLength = 8
  #headerLength = 48
      #utime.sleep_ms(100)
  #readdata()
  #while True:
  #dataunpack(uart1)
  #p1 = Pin(1, Pin.OUT) 
  do_connect()
  
  
  url = 'http://quan.suning.com/getSysTime.do'
  res=urequests.get(url).text
  print(res[13:32])
  shen()
  
 
  #time=t2_date+' '+t2_time
