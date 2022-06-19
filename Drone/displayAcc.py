from imu import MPU6050
import utime
from machine import Pin, I2C, SPI
from ST7735 import TFT
from sysfont import sysfont

ic2 = I2C(0, sda=Pin(8), scl=Pin(9), freq=400000)
imu = MPU6050(ic2)

spi = SPI(1, baudrate=20000000, polarity = 0, phase=0, sck = Pin(10), mosi=Pin(11), miso=Pin(12))
g = 9.81

tft = TFT(spi,14,15,13)
tft.initg()
tft.rgb(True)

tft.fill(TFT.WHITE)
tft.text((10,10), " Acc | rot", TFT.RED, sysfont, 2, nowrap=True)
tft.text((10,30), "==========", TFT.RED, sysfont, 2, nowrap=True)

print("  ACCELERATION (m/s²)  |  Rotation(deg/s)")
print("=======================|=================")
print("  X\t  Y\t  Z    |   X\t Y\tZ")

while True:
    Ax = round(imu.accel.x*g,2)
    Ay = round(imu.accel.y*g,2)
    Az = round(imu.accel.z*g,2)
    Rx = round(imu.gyro.x*g,0)
    Ry = round(imu.gyro.y*g,0)
    Rz = round(imu.gyro.z*g,0)
    print("{:.2f}\t{:.2f}\t{:.2f}   |  {:.0f}\t{:.0f}\t{:.0f}".format(Ax, Ay, Az, Rx, Ry, Rz))
    tft.fillrect((0, 50),(127, 77), TFT.WHITE)
    tft.text((10,50), "X:{:.1f} | {:.0f}".format(Ax, Rx), TFT.RED, sysfont, 2, nowrap=True)
    tft.text((10,70), "Y:{:.1f} | {:.0f}".format(Ay, Ry), TFT.RED, sysfont, 2, nowrap=True)
    tft.text((10,90), "Z:{:.1f} | {:.0f}".format(Az, Rz), TFT.RED, sysfont, 2, nowrap=True)
    utime.sleep_ms(300)
