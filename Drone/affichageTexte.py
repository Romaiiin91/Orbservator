from ST7735 import TFT
from sysfont import sysfont

from machine import SPI, Pin
spi = SPI(1, baudrate=20000000, polarity = 0, phase=0, sck = Pin(10), mosi=Pin(11), miso=Pin(12))

tft = TFT(spi,14,15,13)
tft.initg()
tft.rgb(True)

tft.fill(TFT.WHITE)
tft.text((10,30), "Orb'ser", TFT.RED, sysfont, 3, nowrap=True)
tft.text((10,50), "vator", TFT.RED, sysfont, 3, nowrap=True)





