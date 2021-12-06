import serial
import time
import threading


class SerialPort:
    message = ''

    def __init__(self, port, buand):
        super(SerialPort, self).__init__()
        self.port = serial.Serial(port, buand)
        self.port.close()
        if not self.port.isOpen():
            self.port.open()

    def port_open(self):
        if not self.port.isOpen():
            self.port.open()

    def port_close(self):
        self.port.close()

    def send_data(self):
        data = input("请输入要发送的数据（非中文）并同时接收数据: ")
        n = self.port.write((data + '\n').encode())
        return n

    def read_data(self):
        while True:
            print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))
            numBytes = 4666

            self.dataIn = self.port.read(numBytes)
            # self.message = self.port.readline()
            print(self.dataIn)
            self.port.reset_input_buffer()


serialPort = "COM13"  # 串口
baudRate = 921600  # 波特率

if __name__ == '__main__':

    mSerial = SerialPort(serialPort, baudRate)
    t1 = threading.Thread(target=mSerial.read_data)
    t1.start()


