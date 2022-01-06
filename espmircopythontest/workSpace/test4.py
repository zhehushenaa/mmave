from machine import UART,Pin
import utime
from machine import ADC
# 初始化一个UART对象
uart = UART(1, baudrate=115200, rx=13,tx=12,timeout=10)
#uart.init(9600, bits=8, parity=None, stop=1) # init with given parameters 使用给定参数初始化

count = 1


uart1 = UART(2, baudrate=115200, rx=16,tx=17,timeout=10)


#print(uart1.read())
#print(uart1.any())
print(uart.any())
print(".///")
#with open('ISK_6m_default.cfg','r') as f:
  
  #for line in f.readlines():
    #print(line) # 把末尾的'\n'删掉
    #uart.write(line)      #发送字符串“xianyu”
    #utime.sleep_ms(100)

def ByteToHex( bins ):
    return ''.join( [ "%02X" % x for x in bins ] ).strip()
 
while True:
    if (uart1.any()):
        temp = uart1.read(1000)
        print(temp)
        print("..............")
        print("-------------")
        print ("\n")









