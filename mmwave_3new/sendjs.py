import serial
import time


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



def parserdata():
    numBytes = 4666
    tlvHeaderLength = 8
    headerLength = 48
    # set_output_buffer()
#     print("parserdata")

    dataIn = dataCom.read(numBytes)
    dataCom.reset_input_buffer()
    return  dataIn

if __name__ == '__main__':

    # serial = serial.Serial('COM10', 921600, timeout=0.5) #/dev/ttyUSB0
    # dataCom = serial.Serial('/dev/ttyACM1', 921600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=0.1)
    # uartCom = serial.Serial('/dev/ttyACM0', 115200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=0.2)
    dataCom = serial.Serial('COM13', 921600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=0.1)
    uartCom = serial.Serial('COM12', 115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=0.2)
    poszlist = []
    velzlist = []
    acczlist = []
    numBytes = 4666
    #
    # if uartCom.isOpen():
    #     print("uartcom open success!")
    #     sendCfg()
    # else:
    #     print("uartcom open failed ")

    while True:

        # set_output_buffer()
        #     print("parserdata")

        dataIn = dataCom.read(numBytes)
        dataCom.reset_input_buffer()
        print (dataIn)
        print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))