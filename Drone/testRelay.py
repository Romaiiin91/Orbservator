import utime
from machine import Pin

Relay = Pin(26, Pin.OUT) #connecter sur CN5

while True:
    Relay.value(1) #OFF
    utime.sleep(2)
    Relay.value(0) #ON
    utime.sleep(2)