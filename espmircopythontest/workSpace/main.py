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

def sendcfg():
   uart = UART(1, baudrate=115200, rx=13,tx=12,timeout=10)
   with open('ISK_6m_default.cfg','r') as f:
       for line in f.readlines():
           print(line) # 把末尾的'\n'删掉
           uart.write(line)      #发送字符串“xianyu”
           utime.sleep_ms(100)

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
      print('disconnect')
      utime.sleep(2)
      print(sta_if.isconnected())
      

      sta_if.connect(essid, password)
      retry_times = 30
      while not sta_if.isconnected() and retry_times > 0:
          print(" wait a moment i will try %s items,please" % retry_times)
          utime.sleep(2)
          retry_times -= 1
  if not sta_if.isconnected():
      print('connecting to network...')
      sta_if.connect(essid, password)
      retry_times = 30
      while not sta_if.isconnected() and retry_times > 0:
          print(" wait a moment i will try %s items,please" % retry_times)
          utime.sleep(2)
          retry_times -= 1
  print(sta_if.isconnected())
  print('network config:', sta_if.ifconfig())



def setmytime():
  url = 'http://quan.suning.com/getSysTime.do'
  res=urequests.get(url).text
  #print(res)
  j=ujson.loads(res)
  t2_date = j['sysTime2'].split()[0] #日期
  t2_time = j['sysTime2'].split()[1] #时间
  t_time=t2_date+' '+t2_time
  return t_time




def tlvHeaderDecode(data):
    #print(len(data))
  tlvType, tlvLength = ustruct.unpack('2I', data)
  return tlvType, tlvLength

def DetectedTracks(dataIn, tlvLength):
  P=0
  pmessage={}
  posZ=0
  i=0
  targetStruct = 'I27f'

  targetSize = ustruct.calcsize(targetStruct)
  # print (tlvLength)
  numDetectedTarget = int(tlvLength / targetSize)
      
      
  tid, posX, posY, posZ, velX, velY, velZ, accX, accY, accZ=  ustruct.unpack('I9f', dataIn[:40])
      # print ("tid:",str(tid))
      # print ("posX:",str(posX))
      # print ("posY:",str(posY))
      # print ("posZ:",str(posZ))
      #
      # print ("velZ:",str(velZ))
      # print ("accZ:",str(accZ))
  P=0
  posX=round(posX,2)
    # posX=posX+5
  posY=round(posY,2)
  posZ=round(posZ,4)
  velZ=round(velZ,4)
  accZ=round(accZ,4)
# print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))

# print ("距离：")
# lll=(posX*posX)+(posY*posY)
#print (posZ)



  tempdict={i:(posX,posY,posZ,velZ,accZ,P)}
#  tempdict={peopleid:(posX,posY,P)}
  pmessage.update(tempdict)

  # print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))
  print ("peoplenum:")
  print (numDetectedTarget)
  return pmessage



def dataunpack(dataIn):
  tlvHeaderLength = 8
  headerLength = 48
  #dataIn=b'\x02\x01\x04\x03\x06\x05\x08\x07\x04\x00\x05\x03\x82\x01\x00\x00Ch\n\x00\xd6\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xee5\x00\x00)\x01\x00\x00\xf19\x00\x00\x03\x002\x11\x07\x00\x00\x00x\x00\x00\x00\x00\x00\x00\x00\x92\x0b\x0f>%\x9fG?\x90\xc4\xdc\xbd\xd8d\x18\xbd\x86\xb1\x19\xbf^\xeb(\xbe\n[L=\x0cgN\xbe\xe9:\xfe\xbd<\x82\xc8?Q|F\xbd\xddyI\xbdZ\xd3\xc4\xbcQ|F\xbd\x14h9@\x1cu\x9f\xbd\r\xc0=\xbd\xddyI\xbd\x1cu\x9f\xbd\xd4\xbd8@\x1f\xef\xe7\xbcX\xd3\xc4\xbc\r\xc0=\xbd\x1f\xef\xe7\xbc\xfc!\xc3?\x00\x00@@\xd9\xef\x7f?'
  pmessage={}
  if dataIn:
      #print("字节长度：")
      #print(len(dataIn))
      if dataIn[:8] == b'\x02\x01\x04\x03\x06\x05\x08\x07' and len(dataIn)>167:
          
          
          #magic, version, packetLength, platform, frameNum, subFrameNum, chirpMargin, frameMargin, uartSentTime, trackProcessTime, numTLVs, checksum = ustruct.unpack('Q9I2H', dataIn[:48])
          #print (magic,version,packetLength,platform,frameNum,subFrameNum)
          #print(len(dataIn))
          dataIn = dataIn[48:]
      #print("numTLVs:", numTLVs)
          tlvType, tlvLength = tlvHeaderDecode(dataIn[:tlvHeaderLength])
      
          dataIn = dataIn[tlvHeaderLength:]
          dataLength = tlvLength - tlvHeaderLength
          pmessage = DetectedTracks(dataIn[:dataLength], dataLength)
  return pmessage
    




def fall_detection(pmlist):

  fallbit=0
  height=-1
  posxlist=[]
  posylist=[]
  dislist=[]
  poszlist=[]
  velzlist=[]
  acczlist=[]
  poszavg=100
  velavg=100
  accavg=100
  dis=0


  num=0
  #print(pmlist)

      # print("距离:", str(math.sqrt((x * x) + (y * y))))
  # pmlist={{0,(0,0,0,0,0,0)}}
  for i in pmlist:
      if i != None:
          num=num+1
          if len(i)<2:
              for k,v in i.items():
                  #print(k, v)
                  #print(v[2])
                  posxlist.append(v[0])
                  posylist.append(v[1])
                  poszlist.append(v[2])
                  velzlist.append(v[3])
                  acczlist.append(v[4])
  if num>0:

          poszavg = (sum(poszlist)) / num
          velavg = (sum(velzlist)) / num
          accavg = (sum(acczlist)) / num
          for ix,iy in zip(posxlist,posylist):
              dis=((ix**2)+(iy**2))**0.5
              dislist.append(dis)
    
  #print(posavg)
  #print(velavg)
  # if posavg<=height:
  #     print("跌倒未起！！")
  #     sleep(5)
  if (poszavg <= -0.15 and velavg <= -0.15):
      # for i in range(len(turtleList)):
      #     turtleList[i].pencolor("red")
      if max(dislist)-min(dislist)<0.1 and max(dislist)-min(dislist)>0:
          print("down!!down!")
          #print(max(dislist))
          #print(min(dislist))

          #print(poszavg)
          #print(velavg)
          height=poszavg
          fallbit=1
          # sleep(5)
          utime.sleep(5)
      return fallbit
  else:
      fallbit=0
      return fallbit


def sendfall(fallbit):
  url = 'https://apps.game.qq.com/CommArticle/app/reg/gdate.php'
  url2 = 'http://quan.suning.com/getSysTime.do'
  
  try:
      
      res=urequests.get(url).text

      time=res[20:-2]
  except:
      #with open("test.log","a") as f:
        
        #f.write("fall time error!")
        #f.write("\n")
      utime.sleep(2)
      #do_connect()
      time = '0-0-0 0:0:0'
      #res1=urequests.get(url2).text
      print("time got failed!")
      #time=res1[13:32]
  
  msg={
  "AuthWfpUser":"1",
  "AuthTimeStamp":"2",
  "AuthSign":"3",
  "EquipmentId":"12345678",
  "EquipmentType":"1",
  "AlarmStatus":fallbit,
  "AlarmTime":time
  } 
  msg = ujson.dumps(msg)
  try:
      
      response = urequests.post("http://radar.kinsol.net/api/fall/alarm", data = msg)
      print(time)
      print(response.text)
      print("success!")
  except:
      #with open("test.log","a") as f:
          #f.write("fall upload error!")
          #f.write("\n")
      print("downdata upload failed!")
  #print(type(parsed))

  utime.sleep(2)

  


def senddata():
  tlvHeaderLength = 8
  headerLength = 48
  uart1 = UART(2, baudrate=115200, rx=16,tx=17,timeout=10)

  while True:
      #url = 'http://quan.suning.com/getSysTime.do'
      #res=urequests.get(url).text
      #print(res)
      #j=ujson.loads(res)
      #t2_date = j['sysTime2'].split()[0] #日期
      #t2_time = j['sysTime2'].split()[1] #时间
      #stime=t2_date+' '+t2_time
      #time="2021-12-20 17:02:30"

      # updatex = []
      # updatey = []
      pmlist = []
      fallbit=0
      # parserdata()
      for i in range(25):
          

          #dataIn=b'\x02\x01\x04\x03\x06\x05\x08\x07\x04\x00\x05\x03\x82\x01\x00\x00Ch\n\x00\xd6\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xee5\x00\x00)\x01\x00\x00\xf19\x00\x00\x03\x002\x11\x07\x00\x00\x00x\x00\x00\x00\x00\x00\x00\x00\x92\x0b\x0f>%\x9fG?\x90\xc4\xdc\xbd\xd8d\x18\xbd\x86\xb1\x19\xbf^\xeb(\xbe\n[L=\x0cgN\xbe\xe9:\xfe\xbd<\x82\xc8?Q|F\xbd\xddyI\xbdZ\xd3\xc4\xbcQ|F\xbd\x14h9@\x1cu\x9f\xbd\r\xc0=\xbd\xddyI\xbd\x1cu\x9f\xbd\xd4\xbd8@\x1f\xef\xe7\xbcX\xd3\xc4\xbc\r\xc0=\xbd\x1f\xef\xe7\xbc\xfc!\xc3?\x00\x00@@\xd9\xef\x7f?'
            
          dataIn = uart1.read(1000)
          #print(dataIn)
          #print("..............")
          #pmessage={}
          pmessage=dataunpack(dataIn)
          if pmessage:
            pmlist.append(pmessage)
      if pmlist != None:
          fallbit=fall_detection(pmlist)
          if fallbit==1:
              print("down!")

              sendfall(fallbit)

              utime.sleep(2)

      #print(pmlist)
      #print("跌倒标志位",str(fallbit))
      #print(".....")
      #print("----")
      utime.sleep_ms(50)
      #print("发送时间：",str(time))



def readdata():
    uart1 = UART(2, baudrate=115200, rx=16,tx=17,timeout=10)
    while True:
        if (uart1.any()):
            temp = uart1.read(400)
            print(temp)
            print("..............")
            print("-------------")
            print ("\n")
            
            
            
def sendheartbeat():

    hburl="http://radar.kinsol.net/api/heartbeat"
    url = 'https://apps.game.qq.com/CommArticle/app/reg/gdate.php'
    url2 = 'http://quan.suning.com/getSysTime.do'
    
    while True:
        

        try:
            #print("111")
            res=urequests.get(url2).json()
            #print("222")
            #time=texttime[20:-2]
            

            #res1=urequests.get(url2).text
              #print(res)
            time=res["sysTime2"]

        except:
            print("time got failed！")
            utime.sleep(5)

            time="0-0-0 0:0:0"

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

        #with open("heatbeat.log", "a") as f:
            #f.write(str(msg))
            #f.write("\n")
        js = ujson.dumps(msg)

        try:
            response = urequests.post(hburl, data=js)
            rescode = response.text
            rescode = rescode[8:11]
            if rescode == "200":
                print("heartbeat send success")
            else:
                print("heartbeat send failed")    
        
        except:
            #with open("test.log","a") as f:
                #f.write(time)
                #f.write("heartbeat upload error!")
                #f.write("\n")
            #do_connect()
            print("heartbeat upload failed!")
        print(time)
        #print(msg)
        utime.sleep(10)


            
 
  
if __name__ == '__main__':
  #连接WiFi
  essid = "test"
  password = "henganzhuoyue"
  #tlvHeaderLength = 8
  #headerLength = 48
      #utime.sleep_ms(100)
  #sendcfg()
  #readdata()
  #while True:
  #dataunpack(uart1)
  #p1 = Pin(1, Pin.OUT) 
  do_connect()
  sendcfg()
  #utime.sleep(5)
  
  
  #senddata()

  _thread.start_new_thread(senddata,())
  _thread.start_new_thread(sendheartbeat,())

  #dataunpack()

  #sendheartbeat()

  print("end!")



















