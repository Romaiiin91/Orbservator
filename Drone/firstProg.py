from machine import Pin
import utime

Dot = 0.25
Dash = 1.0
Gap = 0.2
ON = 0
OFF = 1

YLED = Pin(18, Pin.OUT)

while True:
    for i in range(0,3):
        YLED.value(ON)
        utime.sleep(Dot)
        YLED.value(OFF)
        utime.sleep(Gap)
        
    utime.sleep(0.5)
    
    for i in range(0,3):
        YLED.value(ON)
        utime.sleep(Dash)
        YLED.value(OFF)
        utime.sleep(Gap)
        
    utime.sleep(0.5)
    
    for i in range(0,3):
        YLED.value(ON)
        utime.sleep(Dot)
        YLED.value(OFF)
        utime.sleep(Gap)
        
    utime.sleep(2)