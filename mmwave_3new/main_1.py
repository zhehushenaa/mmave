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



ppp = 0
P = 0
bit = 1
alarm = 0
peoplep = 0
poszsum = 0
velzsum = 0
acczsum = 0
nopeopletime = 0
originalbitheight = 0
oldx = []
oldy = []
turtleList = []


poszlist = []
velzlist = []
acczlist = []
maxPoints = 1150

allmaxpoints=[]

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



# def parsePointcloud(dataIn,tlvLength):
#     global allmaxpoints
#     ttt=[]
#
#
#     pUnitStruct = '5f'  # elev, azim, doppler, range, snr
#     pUnitSize = struct.calcsize(pUnitStruct)
#     pUnit = struct.unpack(pUnitStruct, dataIn[:pUnitSize])
#     dataIn = dataIn[pUnitSize:]
#     objStruct = '2bh2H'  # 2 int8, 1 int16, 2 uint16
#     objSize = struct.calcsize(objStruct)
#     numDetectedObj = int((tlvLength - pUnitSize) / objSize)
#     pcPolar = np.zeros((5, maxPoints))
#     # if (self.printVerbosity == 1):
#     print('Parsed Points: ', numDetectedObj)
#     for i in range(numDetectedObj):
#         try:
#             elev, az, doppler, ran, snr = struct.unpack(objStruct, dataIn[:objSize])
#             dataIn = dataIn[objSize:]
#             # get range, azimuth, doppler, snr
#             pcPolar[0, i] = ran * pUnit[3]
#             if (az >= 128):
#                 print('Az greater than 127')
#                 az -= 256
#             if (elev >= 128):
#                 print('Elev greater than 127')
#                 elev -= 256
#             if (doppler >= 32768):
#                 print('Doppler greater than 32768')
#                 doppler -= 65536
#
#             pcPolar[1, i] = az * pUnit[1]  # azimuth
#             pcPolar[2, i] = elev * pUnit[0]  # elevation
#             pcPolar[3, i] = doppler * pUnit[2]  # doppler
#             pcPolar[4, i] = snr * pUnit[4]  # snr
#         except:
#                 # numDectedObj = i
#                 print('failed to get point cloud')
#                 break
#
#
#
#     pcBufPing = np.empty((5,numDetectedObj))
#     for n in range(0, numDetectedObj):
#         pcBufPing[2,n] = pcPolar[0,n]*math.sin(pcPolar[2,n]) #z
#         pcBufPing[0,n] = pcPolar[0,n]*math.cos(pcPolar[2,n])*math.sin(pcPolar[1,n]) #x
#         pcBufPing[1,n] = pcPolar[0,n]*math.cos(pcPolar[2,n])*math.cos(pcPolar[1,n]) #y
#     pcBufPing[3,:] = pcPolar[3,0:numDetectedObj] #doppler
#     pcBufPing[4,:] = pcPolar[4,0:numDetectedObj] #snr
#
#
#     for n in range(0, numDetectedObj):
#         ttt.append(pcBufPing[2,n])
#         # print(pcBufPing[3, n])
#         # print(pcBufPing[4, n])
#     # print ("????????????")
#     # print (max(ttt))
#     # # allmaxpoints=[]
#     # allmaxpoints.append(max(ttt))
#     # if len(allmaxpoints)>=30:
#     #     print ("....")
#     #     if allmaxpoints[28]>(allmaxpoints[29]+0.5):
#     #         print ("???????????????")
#     #
#     #     # print ("???????????????")
#     #     # print ((sum(allmaxpoints[:15]))/15-max(ttt))
#     #     allmaxpoints=allmaxpoints[1:]





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

        # print ("?????????")
        # lll=(posX*posX)+(posY*posY)
        print (posZ)


        
        tempdict={i:(posX,posY,posZ,velZ,accZ,P)}
       #  tempdict={peopleid:(posX,posY,P)}
        pmessage.update(tempdict)

    # print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))
    print ("???????????????")
    print (numDetectedTarget)
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
        print("numTLVs:", numTLVs)
        tlvType, tlvLength = tlvHeaderDecode(dataIn[:tlvHeaderLength])

        dataIn = dataIn[tlvHeaderLength:]
        dataLength = tlvLength - tlvHeaderLength
        print (tlvType)
        if (tlvType == 7):

            print (len(dataIn))
            print("wennwennwne")
            pmessage = parseDetectedTracksSDK3x(dataIn[:dataLength], dataLength)
        # pmessage={0: (0.14, 0.78, -0.1078, -0.165, -0.1241, 0)}
            print (pmessage)
            return pmessage
        else:
            pmessage={}
            return pmessage

            # dataLength = tlvLength - tlvHeaderLength

        # except:
        #     print('TLV Header Parsing Failure')


        # for i in range(numTLVs):
        #     # try:
        #     # print("DataIn Type", type(dataIn))
        #     try:
        #         # print("<<<<<<")
        #         # print(dataIn)
        #         # print(">>>>>>")
        #         tlvType, tlvLength = tlvHeaderDecode(dataIn[:tlvHeaderLength])
        #
        #         dataIn = dataIn[tlvHeaderLength:]
        #
        #         dataLength = tlvLength - tlvHeaderLength
        #
        #     except:
        #         print('TLV Header Parsing Failure')
        #         fail = 1
        #         # return dataIn
        #     if (tlvType == 6):
        #         print("-----2")
        #         parsePointcloud(dataIn[:dataLength], dataLength)
        #
        #         # DPIF Polar Coordinates
        #         # self.parseCapon3DPolar(dataIn[:dataLength], dataLength)
        #     elif (tlvType == 7):
        #
        #         # target 3D
        #         # a = a + 1
        #         pmessage=parseDetectedTracksSDK3x(dataIn[:dataLength], dataLength)
        #         # print (pmessage)
        #         return pmessage
        #
        #     dataIn = dataIn[dataLength:]

# ????????????
def turtledisplay(tdata):
    global bit
    print ("tdata")
    print (tdata)
    if bit == 1:
        for k, v in tdata.items():
            x = int(v[0] * 100)
            y = int(v[1] * 100)
            oldx.append(x)
            oldy.append(y)
            print("=========")

        bit=0
    for i in range(len(tdata)):
        turtleList.append(turtle.Turtle(shape='turtle'))
        # turtleList[i].speed('normal')
    for k, v in tdata.items():
        x = int(v[0] * 100)
        y = int(v[1] * 100)

        if len(tdata) <= len(oldx):
            if abs(x - oldx[k]) < 1 or abs(y - oldy[k]) < 1:
                updatex.append(oldx[k])
                updatey.append(oldy[k])
            else:
                updatex.append(x)
                updatey.append(y)

        else:
            updatex.append(x)
            updatey.append(y)

        for i in range(len(updatex)):
            # turtleList[i].showturtle()
            turtleList[i].penup()

            print ("updatex,updatey:")
            print (updatex[i],updatey[i])
            turtleList[i].goto(updatex[i], updatey[i])

            # turtle.speed(3)
            # turtleList[i].delay(10)
        oldx.clear()
        oldy.clear()
        print("len:", str(len(updatex)))

        for i in range(len(updatex)):
            oldx.append(updatex[i])
            oldy.append(updatey[i])





def fall_detection(data):

    global ppp

    global poszlist
    global velzlist
    global acczlist

    for k, v in data.items():
        pass

    poszlist.append(v[2])
    velzlist.append(v[3])
    acczlist.append(v[4])

    if ppp == 9:
        # print("??????:", str(math.sqrt((x * x) + (y * y))))
        posavg = (sum(poszlist)) / 10
        velavg = (sum(velzlist)) / 10
        accavg = (sum(acczlist)) / 10

        poszlist = []
        velzlist = []
        acczlist = []
        # print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))
        print("10?????????????????????", posavg)
        print("10???????????????????????????", velavg)
        print("10????????????????????????", accavg)
        if (accavg <= -0.1 or velavg <= -0.1):
            for i in range(len(turtleList)):
                turtleList[i].pencolor("red")
            print("????????????????????????")
            print("????????????")
            print("????????????")
            P = 2
            alarm = 1
        # if posavg > 0.5 * originalheight:
        #     timepiece = 0

        # if timepiece > 20:
        #     if posavg <= 0.3 * originalheight:
        #         for i in range(len(turtleList)):
        #             turtleList[i].pencolor("red")
        #         print("????????????????????????")
        #         P = 2
        #                             timepiece=0

        # if poszsum/15<=0.3:
        # print ("????????????")
        # P = 1
        # if posavg >= 0.5 * originalheight:
        #     for i in range(len(turtleList)):
        #         turtleList[i].pencolor("black")
        #     print("??????!!")
        #     P = 0



        ppp = 0




# ????????????
def senddataweb():
    url="http://radar.kinsol.net/api/fall/alarm"
    Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    msg= {
            "AuthWfpUser": "klwab1iqcl38rf5ggxquku4lx",
            "AuthTimeStamp": "7st4nhn7l6fd26a6yzdmp23uh",
            "AuthSign": "6137c30fe9b7b3adfb5da9fccf6383bcb387f3897ca0259651ee58b02d33738e1c60e95c7343fdb6703e116e611ee1d9659a608595ad615ed3065441c4cd2d8a",
            "EquipmentId": "12345678",
            "EquipmentType": "1",
            "AlarmStatus": "1",
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
            print("?????????????????????")
        else:
            print("??????????????????")

            # break
    except:
        print("?????????")
    sleep(5)



# def senddataweb(pm,P,alarm):
#     # print (pm)
#     appid = "Tz6HqcR97CL9A8CqTim82ZIkZGFMBQ1h"
#     secret = "sX4nhO2IHxcmuTaTwMtg6hGh2Ab1NdPE"
#
#     newdate= "2021051905551155"
#     jdata=appid+secret+newdate
#     md5=hashlib.md5()
#     md5.update(jdata.encode("GB2312"))
#     jdata=md5.hexdigest()
#     deviceid="11223344556677"
#     current_timestamp=datetime.datetime.now()
#     testdate1=current_timestamp.strftime("%Y-%m-%d %H:%M:%S")
#     PeopleNum = 1
#
#     People1='0.00,0.00,0'
#     People2='0.00,0.00,0'
#     People3='0.00,0.00,0'
#     People4='0.00,0.00,0'
#     People5='0.00,0.00,0'
#     People6='0.00,0.00,0'
#     People7='0.00,0.00,0'
#     People8='0.00,0.00,0'
#     if pm is None:
#         pass
#         # print ("no pmessage!")
#         # PeopleNum = 0
#     else:
#         for p,v in pm.items():
#             if PeopleNum==1:
#                 People1=str(v).replace("(","").replace(")","")
#                 People1=People1[:10]+","+str(P)
#             if PeopleNum==2:
#                 People2=str(v).replace("(","").replace(")","")
#                 People2=People2[:10]+","+str(P)
#             if PeopleNum==3:
#                 People3=str(v).replace("(","").replace(")","")
#                 People3=People3[:10]+","+str(P)
#             if PeopleNum==4:
#                 People4=str(v).replace("(","").replace(")","")
#                 People4=People4[:10]+","+str(P)
#             if PeopleNum==5:
#                 People5=str(v).replace("(","").replace(")","")
#                 People5=People5[:10]+","+str(P)
#             if PeopleNum==6:
#                 People6=str(v).replace("(","").replace(")","")
#                 People6=People6[:10]+","+str(P)
#             if PeopleNum==7:
#                 People7=str(v).replace("(","").replace(")","")
#                 People7=People7[:10]+","+str(P)
#             if PeopleNum==8:
#                 People8=str(v).replace("(","").replace(")","")
#                 People8=People8[:10]+","+str(P)
#             PeopleNum = PeopleNum+1
#
#     Alarm=str(PeopleNum-1)+","+str(alarm)
# #     Alarm="1,1"
# #     print ("--------")
# #     print (Alarm)
#     Other="??????????????????"
#
#
#
#     headers={"appid":appid,"timestamp":newdate,"sign":jdata}
#     # bb = {"deviceId": deviceid, "time": testdate1, "PeopleNum": PeopleNum, "People1": People1, "People2": People2,
#     #     "People3": People3, "People4": People4, "People5": People5, "People6": People6, "People7": People7,
#     #     "People8": People8, "Other": Other}
#
#     bb = {"deviceId": deviceid, "time": testdate1, "PeopleNum": PeopleNum-1, "People1": People1, "People2": People2,
#         "People3": People3, "People4": People4, "People5": People5, "People6": People6, "People7": People7,
#         "People8": People8,"Alarm":Alarm,"Other": Other}
#     js = json.dumps(bb)
#     url="http://27.115.85.150:10016/Millimeter_wave_radar_PersonPos.ashx"
#     try :
#         response=requests.post(url,data=js,headers=headers,timeout=300)
#         print(bb)
#         print (response.text)
#     except:
#         print ("?????????")
#     time.sleep(0.05)


# def senddataweb_test():
#     # print (pm)
#     appid = "Tz6HqcR97CL9A8CqTim82ZIkZGFMBQ1h"
#     secret = "sX4nhO2IHxcmuTaTwMtg6hGh2Ab1NdPE"
#
#     newdate= "2021051905551155"
#     jdata=appid+secret+newdate
#     md5=hashlib.md5()
#     md5.update(jdata.encode("GB2312"))
#     jdata=md5.hexdigest()
#     deviceid="11223344556677"
#     current_timestamp=datetime.datetime.now()
#     testdate1=current_timestamp.strftime("%Y-%m-%d %H:%M:%S")
#     PeopleNum = 1
#
#     People1='0.00,0.00,0'
#     People2='0.00,0.00,0'
#     People3='0.00,0.00,0'
#     People4='0.00,0.00,0'
#     People5='0.00,0.00,0'
#     People6='0.00,0.00,0'
#     People7='0.00,0.00,0'
#     People8='0.00,0.00,0'
#
#
#     Alarm=str(PeopleNum-1)+","+str(alarm)
# #     Alarm="1,1"
# #     print ("--------")
# #     print (Alarm)
#     Other="??????????????????"
#
#
#
#     headers={"appid":appid,"timestamp":newdate,"sign":jdata}
#     # bb = {"deviceId": deviceid, "time": testdate1, "PeopleNum": PeopleNum, "People1": People1, "People2": People2,
#     #     "People3": People3, "People4": People4, "People5": People5, "People6": People6, "People7": People7,
#     #     "People8": People8, "Other": Other}
#
#     bb = {"deviceId": deviceid, "time": testdate1, "PeopleNum": PeopleNum-1, "People1": People1, "People2": People2,
#         "People3": People3, "People4": People4, "People5": People5, "People6": People6, "People7": People7,
#         "People8": People8,"Alarm":Alarm,"Other": Other}
#     bb={"deviceId": "0", "time": "0","PeopleNum": "0", "People1": "0", "People2": "0",
#         "People3": "0", "People4": "0","People5": "0",
#         "Alarm":"0","Other": "0"}
#     js = json.dumps(bb)
#     url="http://27.115.85.150:10016/Millimeter_wave_radar_PersonPos.ashx"
#     try :
#         response=requests.post(url,data=js,headers=headers,timeout=300)
#         print(bb)
#         print (response.text)
#     except:
#         print ("?????????")
#     time.sleep(0.3)


if __name__ == '__main__':
  
    # serial = serial.Serial('COM10', 921600, timeout=0.5) #/dev/ttyUSB0
    # dataCom = serial.Serial('/dev/ttyACM1', 921600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=0.1)
    # uartCom = serial.Serial('/dev/ttyACM0', 115200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=0.2)
    dataCom = serial.Serial('COM10', 115200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=0.05)
    uartCom = serial.Serial('COM11', 115200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=0.2)
    poszlist=[]
    velzlist=[]
    acczlist=[]
    pmlist=[]

    # if uartCom.isOpen():
    #      print ("uartcom open success!")
    #      sendCfg()
    # else:
    #      print ("uartcom open failed ")

    # senddataweb_test()
    if dataCom.isOpen() :
        print(" datacom open success!")
        while True:
            updatex = []
            updatey = []

            # parserdata()
            for i in range(10):
                pm=parserdata()
                pmlist.append(pm)
            fall_detection()

            # print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))
            #
            if pm is not None:
                nopeopletime = 0
                # fall_detection(pm)
                turtledisplay(pm)
            #     # fall_detection(pm, poszlist, velzlist, acczlist)
            #     senddataweb(pm, P, alarm)
            #     ppp=ppp+1
            else:

                nopeopletime=nopeopletime+1
                if nopeopletime==10:
                    allmaxpoints =[]
                    originalbitheight=0

                    bit=1

                    turtleList=[]

                    turtle.clearscreen()


                    # senddataweb(pm,P,alarm)
    else :
        print(" datacom open failed!")
    # while True:
    #     senddataweb()
    #     time.sleep(2)



    # ss=b'\x02\x01\x04\x03\x06\x05\x08\x07\x04\x00\x05\x03\xb5\x00\x00\x00Ch\n\x00\x104\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xcd/\x00\x00\x1c\x00\x00\x009;\x00\x00\x02\x00\xab\xe4\x07\x00\x00\x00x\x00\x00\x00\x00\x00\x00\x00\xc3\x14\xef>\xbeb4?]\x8dC<\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00O\xcc\xff?\xa4\xd9m\xbd\xefd\xad\xbd\x7fK\x87\xbd\xa4\xd9m\xbd\x8cS\xa4@\x1b\x84\xdf\xbd;\xe6\x1d\xbe\xefd\xad\xbd\x1b\x84\xdf\xbd[B\x9e@\xe9"\xe3\xbd\x7fK\x87\xbd;\xe6\x1d\xbe\xe9"\xe3\xbd^\x9dR@\x00\x00@@\xe0\xff\x7f?\x02\x01\x04\x03\x06\x05\x08\x07'
    # dataIn=b'\x02\x01\x04\x03\x06\x05\x08\x07\x04\x00\x05\x03\x82\x01\x00\x00Ch\n\x00\xd6\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xee5\x00\x00)\x01\x00\x00\xf19\x00\x00\x03\x002\x11\x07\x00\x00\x00x\x00\x00\x00\x00\x00\x00\x00\x92\x0b\x0f>%\x9fG?\x90\xc4\xdc\xbd\xd8d\x18\xbd\x86\xb1\x19\xbf^\xeb(\xbe\n[L=\x0cgN\xbe\xe9:\xfe\xbd<\x82\xc8?Q|F\xbd\xddyI\xbdZ\xd3\xc4\xbcQ|F\xbd\x14h9@\x1cu\x9f\xbd\r\xc0=\xbd\xddyI\xbd\x1cu\x9f\xbd\xd4\xbd8@\x1f\xef\xe7\xbcX\xd3\xc4\xbc\r\xc0=\xbd\x1f\xef\xe7\xbc\xfc!\xc3?\x00\x00@@\xd9\xef\x7f?'
    #
    # magic, version, packetLength, platform, frameNum, subFrameNum, chirpMargin, frameMargin, uartSentTime, trackProcessTime, numTLVs, checksum = struct.unpack('Q9I2H', dataIn[:48])
    # print (magic,version,packetLength,platform,frameNum,subFrameNum)
    # print(len(dataIn))
    # dataIn = dataIn[48:]
    # print("numTLVs:", numTLVs)