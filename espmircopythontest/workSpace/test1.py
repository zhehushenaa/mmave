#板载LED（GPIO1）1秒闪烁测试 
from machine import Pin
import time
p1 = Pin(1, Pin.OUT)    # create output pin on GPIO4
while True:
    p1.value(0)             # set pin to high level
    time.sleep(1)           # sleep for 1 second
    p1.value(1)             # set pin to low level
    time.sleep(1)           # sleep for 1 second
    
