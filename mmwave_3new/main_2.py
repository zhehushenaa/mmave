## -*- coding: utf-8 -*-
import serial
from time import sleep
import struct
import requests
import json
import hashlib
import datetime
import time
import turtle
import math
import numpy as np
import threading





def sendCfg():
    with open('ISK_6m_default.cfg', 'r') as cfg:
        for line in cfg:
            time.sleep(.1)
            uartCom.write(line.encode())
            ack = uartCom.readline()
            #print("m1")
            print(ack)
            #print("m2")
            ack = uartCom.readline()
            print(ack)
            #print("m3")
    time.sleep(3)
    uartCom.reset_input_buffer()
    uartCom.close()


# def recv(serial):
#
#   while True:
#     data = serial.read_all()
#     if data == '':
#       continue
#     else:
#       break
#     sleep(0.01)
#   return data


def tlvHeaderDecode(data):
    #print(len(data))
  tlvType, tlvLength = struct.unpack('2I', data)
  return tlvType, tlvLength








def parseDetectedTracksSDK3x(dataIn, tlvLength):

      #targetStruct = 'I15f'
    P=0
    pmessage={}
    posZ=0
    targetStruct = 'I27f'
    targetSize = struct.calcsize(targetStruct)
    # print (tlvLength)
    numDetectedTarget = int(tlvLength / targetSize)
    for i in range(numDetectedTarget):
        tid, posX, posY, posZ, velX, velY, velZ, accX, accY, accZ=  struct.unpack('I9f', dataIn[:40])
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
        # print (posZ)


        
        tempdict={i:(posX,posY,posZ,velZ,accZ,P)}
       #  tempdict={peopleid:(posX,posY,P)}
        pmessage.update(tempdict)

    # print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))
    # print ("人物个数：")
    # print (numDetectedTarget)
    return pmessage


def parserdata():
    numBytes = 4666
    tlvHeaderLength = 8
    headerLength = 48
    # set_output_buffer()
#     print("parserdata")

    dataIn = dataCom.read(numBytes)
    dataCom.reset_input_buffer()
    # print (dataIn)
    # print ("datalen:",len(dataIn))
    # print (dataIn[:8])
    # print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))

    if dataIn[:8] == b'\x02\x01\x04\x03\x06\x05\x08\x07' and len(dataIn)>108:



        # print("<<<<<<")
        # print(dataIn)
        # print(">>>>>>")

        magic, version, packetLength, platform, frameNum, subFrameNum, chirpMargin, frameMargin, uartSentTime, trackProcessTime, numTLVs, checksum = struct.unpack(
            'Q9I2H', dataIn[:headerLength])
        dataIn = dataIn[48:]
        # print("numTLVs:", numTLVs)
        tlvType, tlvLength = tlvHeaderDecode(dataIn[:tlvHeaderLength])

        dataIn = dataIn[tlvHeaderLength:]
        dataLength = tlvLength - tlvHeaderLength
        # print (tlvType)
        if (tlvType == 7):

            # print (len(dataIn))
            # print("wennwennwne")
            pmessage = parseDetectedTracksSDK3x(dataIn[:dataLength], dataLength)
        # pmessage={0: (0.14, 0.78, -0.1078, -0.165, -0.1241, 0)}
        #     print (pmessage)
            return pmessage
        else:
            pmessage={}
            return pmessage



# 显示部分
# def turtledisplay(tdata):
#     global bit
#     print ("tdata")
#     print (tdata)
#     if bit == 1:
#         for k, v in tdata.items():
#             x = int(v[0] * 100)
#             y = int(v[1] * 100)
#             oldx.append(x)
#             oldy.append(y)
#             print("=========")
#
#         bit=0
#     for i in range(len(tdata)):
#         turtleList.append(turtle.Turtle(shape='turtle'))
#         # turtleList[i].speed('normal')
#     for k, v in tdata.items():
#         x = int(v[0] * 100)
#         y = int(v[1] * 100)
#
#         if len(tdata) <= len(oldx):
#             if abs(x - oldx[k]) < 1 or abs(y - oldy[k]) < 1:
#                 updatex.append(oldx[k])
#                 updatey.append(oldy[k])
#             else:
#                 updatex.append(x)
#                 updatey.append(y)
#
#         else:
#             updatex.append(x)
#             updatey.append(y)
#
#         for i in range(len(updatex)):
#             # turtleList[i].showturtle()
#             turtleList[i].penup()
#
#             print ("updatex,updatey:")
#             print (updatex[i],updatey[i])
#             turtleList[i].goto(updatex[i], updatey[i])
#
#             # turtle.speed(3)
#             # turtleList[i].delay(10)
#         oldx.clear()
#         oldy.clear()
#         print("len:", str(len(updatex)))
#
#         for i in range(len(updatex)):
#             oldx.append(updatex[i])
#             oldy.append(updatey[i])





def fall_detection(pmlist):
    global height
    fallbit=0
    height=-1
    poszlist=[]
    velzlist=[]
    acczlist=[]

    posavg=10
    velavg=10
    accavg=10
    Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    num=0
    print(pmlist)

        # print("距离:", str(math.sqrt((x * x) + (y * y))))
    # pmlist={{0,(0,0,0,0,0,0)}}
    for i in pmlist:
        if i != None:
            num=num+1
            if len(i)<2:
                for k,v in i.items():
                    print(k, v)
                    print(v[2])
                    poszlist.append(v[2])
                    velzlist.append(v[3])
                    acczlist.append(v[4])
        if num>0:
            posavg = (sum(poszlist)) / num
            velavg = (sum(velzlist)) / num
            accavg = (sum(acczlist)) / num
    #
    #
    print(Time)
    print(posavg)
    print(velavg)
    # if posavg<=height:
    #     print("跌倒未起！！")
    #     sleep(5)
    if (posavg <= -0.18 and velavg <= -0.18):
        # for i in range(len(turtleList)):
        #     turtleList[i].pencolor("red")
        print("跌倒！！跌倒！！")
        print(posavg)
        print(velavg)

        print("跌倒！！")
        height=posavg
        fallbit=1
        # sleep(5)
        return fallbit
    else:
        fallbit=0
        return fallbit



# 发送数据
def sendfall(fallbit):
    url="http://radar.kinsol.net/api/fall/alarm"
    Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    msg= {
            "AuthWfpUser": "11",
            "AuthTimeStamp": "22",
            "AuthSign": "33",
            "EquipmentId": "12345678",
            "EquipmentType": "1",
            "AlarmStatus": fallbit,
            "AlarmTime": Time
    }
    js = json.dumps(msg)

    try:
        response = requests.post(url, data=js, timeout=50)
        print(msg)
        rescode = response.text
        print(rescode)
        rescode = rescode[8:11]
        print (rescode)
        if rescode == "200":
            print("发送报警成功！")
        else:
            print("发送未成功！")

            # break
    except:
        print("超时！")
    # sleep(3)





def sendheartbeat():
    hburl="http://radar.kinsol.net/api/heartbeat"
    while True:
        Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        msg = {
            "AuthWfpUser": "3",
            "AuthTimeStamp": "2",
            "AuthSign": "1",
            "EquipmentId": "12345678",
            "EquipmentType": "1",
            "EquipmentStatus": "1",
            "peoplecounting": "1",
            "CreationTime": Time
        }

        with open("heatbeat.log", "a") as f:
            f.write(str(msg))
            f.write("\n")
        js = json.dumps(msg)

        try:
            response = requests.post(hburl, data=js,timeout=50)
            print(msg)
            rescode = response.text
            rescode = rescode[8:11]
            if rescode == "200":

                print("发送心跳成功！")
            else:
                print("发送未成功！")

                # break
        except:
            print("超时！")
        sleep(5)

def senddata():

    while True:
        Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


        # updatex = []
        # updatey = []
        pmlist = []
        # parserdata()
        for i in range(25):
            pm=parserdata()
            pmlist.append(pm)
        # print("pmmmmmm")
        # print(pm)
        # print("pppppppppm")
        fallbit=fall_detection(pmlist)
        sendfall(fallbit)
        print("跌倒标志位",str(fallbit))
        print("发送时间：",str(Time))


        # print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))
        #
        # if pm is not None:
        #     nopeopletime = 0
        #     # fall_detection(pm)
        #     turtledisplay(pm)
        # #     # fall_detection(pm, poszlist, velzlist, acczlist)
        # #     senddataweb(pm, P, alarm)
        # #     ppp=ppp+1
        # else:
        #
        #     nopeopletime=nopeopletime+1
        #     if nopeopletime==10:
        #         allmaxpoints =[]
        #         originalbitheight=0
        #
        #         bit=1
        #
        #         turtleList=[]
        #
        #         turtle.clearscreen()


# senddataweb(pm,P,alarm)

if __name__ == '__main__':
  
    # serial = serial.Serial('COM10', 921600, timeout=0.5) #/dev/ttyUSB0
    # dataCom = serial.Serial('/dev/ttyACM1', 921600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=0.1)
    # uartCom = serial.Serial('/dev/ttyACM0', 115200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=0.2)
    # dataCom = serial.Serial('COM10', 115200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=0.05)
    # uartCom = serial.Serial('COM11', 115200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=0.2)
    alarm = 0
    peoplep = 0
    nopeopletime = 0
    originalbitheight = 0
    oldx = []
    oldy = []
    turtleList = []
    # pmlist=[]
    t1 = threading.Thread(target=sendheartbeat)
    t2 = threading.Thread(target=senddata)

    t1.start()

    # if uartCom.isOpen():
    #      print ("uartcom open success!")
    #      sendCfg()
    # else:
    #      print ("uartcom open failed ")
    #
    # # senddataweb_test()
    # if dataCom.isOpen() :
    #     print(" datacom open success!")
    #     # t1.start()
    #     # t2.start()
    #
    # else :
    #     print(" datacom open failed!")



    # ss=b'\x02\x01\x04\x03\x06\x05\x08\x07\x04\x00\x05\x03\xb5\x00\x00\x00Ch\n\x00\x104\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xcd/\x00\x00\x1c\x00\x00\x009;\x00\x00\x02\x00\xab\xe4\x07\x00\x00\x00x\x00\x00\x00\x00\x00\x00\x00\xc3\x14\xef>\xbeb4?]\x8dC<\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00O\xcc\xff?\xa4\xd9m\xbd\xefd\xad\xbd\x7fK\x87\xbd\xa4\xd9m\xbd\x8cS\xa4@\x1b\x84\xdf\xbd;\xe6\x1d\xbe\xefd\xad\xbd\x1b\x84\xdf\xbd[B\x9e@\xe9"\xe3\xbd\x7fK\x87\xbd;\xe6\x1d\xbe\xe9"\xe3\xbd^\x9dR@\x00\x00@@\xe0\xff\x7f?\x02\x01\x04\x03\x06\x05\x08\x07'
    # dataIn=b'\x02\x01\x04\x03\x06\x05\x08\x07\x04\x00\x05\x03\x82\x01\x00\x00Ch\n\x00\xd6\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xee5\x00\x00)\x01\x00\x00\xf19\x00\x00\x03\x002\x11\x07\x00\x00\x00x\x00\x00\x00\x00\x00\x00\x00\x92\x0b\x0f>%\x9fG?\x90\xc4\xdc\xbd\xd8d\x18\xbd\x86\xb1\x19\xbf^\xeb(\xbe\n[L=\x0cgN\xbe\xe9:\xfe\xbd<\x82\xc8?Q|F\xbd\xddyI\xbdZ\xd3\xc4\xbcQ|F\xbd\x14h9@\x1cu\x9f\xbd\r\xc0=\xbd\xddyI\xbd\x1cu\x9f\xbd\xd4\xbd8@\x1f\xef\xe7\xbcX\xd3\xc4\xbc\r\xc0=\xbd\x1f\xef\xe7\xbc\xfc!\xc3?\x00\x00@@\xd9\xef\x7f?'
    #
    # magic, version, packetLength, platform, frameNum, subFrameNum, chirpMargin, frameMargin, uartSentTime, trackProcessTime, numTLVs, checksum = struct.unpack('Q9I2H', dataIn[:48])
    # print (magic,version,packetLength,platform,frameNum,subFrameNum)
    # print(len(dataIn))
    # dataIn = dataIn[48:]
    # print("numTLVs:", numTLVs)