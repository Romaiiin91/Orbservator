from machine import Pin, UART, I2C
import utime
from imu import MPU6050

uart = UART(0, baudrate=115200, rx=Pin(1), tx=Pin(0))
ic2 = I2C(0, sda=Pin(8), scl=Pin(9), freq=400000)
imu = MPU6050(ic2)
g=9.81

# fichier = open("sortieConnect.txt", 'w')

uart = machine.UART(0)

def sendAT(uart, str):
    str+= "\r\n"
    uart.write(str)
    utime.sleen(3)
    while uart.any():
        print(uart.readline())
    utime.sleep(3)
    while uart.any():
        print(uart.readline())
        
# Send command and wait for response
# def sendCMD_waitRespLine(cmd, timeout=2000):
#     print("CMD: " + cmd)
#     fichier.write("CMD: {}\n".format(cmd))
#     cmd +="\r\n"
#     uart.write(cmd)
#     waitRespLine(timeout)
#     print()
#     
# # Walt for response with timeout
# 
# def waitRespLine(timeout=4000):
#     prvMills = utime.ticks_ms()
#     texte = " "
#     while ((utime.ticks_ms() - prvMills) < timeout):
#         if uart.any():
#             fichier.write(uart.readline())
           


# Essai avec decode
def sendCMD_waitRespLine2(cmd, timeout=2000):
    print("CMD: " + cmd)
    cmd +="\r\n"
    uart.write(cmd)
    waitRespLine2(timeout)
    print()
    
# Walt for response with timeout

def waitRespLine2(timeout=4000):
    prvMills = utime.ticks_ms()
    while ((utime.ticks_ms() - prvMills) < timeout):
        if uart.any():
            print(uart.readline().decode('UTF-8'))
            #print("En cours")
#Get version number and turn echo OFF

#sendCMD_waitRespLine2("ATEO")


#Connect to local wi-fi router
sendCMD_waitRespLine2("AT+CWMODE=1")
sendCMD_waitRespLine2("AT+CWJAP=\"iPhone de Romain\",\"12345678\"", timeout=10000)
sendCMD_waitRespLine2("AT+PING=\"www.bbc.co.uk\"",timeout=10000)
sendCMD_waitRespLine2("AT+CIFSR")

print()
print("Over")

sendCMD_waitRespLine2("AT+CIPMUX=0")
sendCMD_waitRespLine2("AT+CIPSTART=\"UDP\",\"0.0.0.0\",5000,5000,2")




# fichier.close()
# 
# fichier = open("sortieConnect.txt", 'r')
# lignes = fichier.readlines()
# fichier.close()
# 
# for ligne in lignes:
#     print(ligne)
    

while True:
    buf = uart.readline()
    if buf :
        dat = buf.decode('UTF-8')
        
        
        
        Ax = round(imu.accel.x*g,2)
        Ay = round(imu.accel.y*g,2)
        Az = round(imu.accel.z*g,2)
    
        Coordstr = "Ax=" + str(Ax) + ", Ay=" + str(Ay) + ", Az=" + str(Az)
        Coordlen= str(len(Coordstr))
        Dt = "AT+CIPSEND="+Coordlen+"\r\n"
        uart.write(Dt)
        utime.sleep_ms(100)
        uart.write(Coordstr)
        sendCMD_waitRespLine2("AT+CIPSTART=\"UDP\",\"0.0.0.0\",5000,5000,2")
