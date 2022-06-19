from imu import MPU6050
import utime
from machine import Pin, I2C, SPI, UART
from ST7735 import TFT
from sysfont import sysfont


####################################################
#
#              Connection
#
####################################################
uart = UART(0, baudrate=115200, rx=Pin(1), tx=Pin(0))
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
        
    
#
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


# N'affiche uart.readline
def sendCMD_waitRespLine3(cmd, timeout=2000):
    print("CMD: " + cmd)
    cmd +="\r\n"
    uart.write(cmd)
    #waitRespLine3(timeout)
    print()
    
# Walt for response with timeout

def waitRespLine3(timeout=4000):
    prvMills = utime.ticks_ms()
    while ((utime.ticks_ms() - prvMills) < timeout):
        if uart.any():
            #print(uart.readline().decode('UTF-8'))
            continue
         
         
def strSend():
    heure = utime.gmtime(utime.time())[:-2]
    text = "{}-{}-{} -- {}h{}:{}\n".format(heure[2], heure[1], heure[0], heure[3], heure[4], heure[5])
    text += "Tps: " + str(T_s) + "\n"
    text += "Tps: " + str(T_s) + "\n"
    text += "Ax: " + str(accMoyenne[0]) +"\n"
    text += "Ay: " + str(accMoyenne[1]) +"\n"
    text += "Az: " + str(accMoyenne[2]) +"\n"
    text += "Vitesse: " + str(vit) +"\n"
    return text


#Turn echo OFF

sendCMD_waitRespLine2("ATEO")

#Connect to local wi-fi router
sendCMD_waitRespLine2("AT+CWMODE=1")
sendCMD_waitRespLine2("AT+CWJAP=\"iPhone de Romain\",\"12345678\"", timeout=10000)
sendCMD_waitRespLine2("AT+PING=\"www.bbc.co.uk\"",timeout=10000)
sendCMD_waitRespLine2("AT+CIFSR")

print()

sendCMD_waitRespLine2("AT+CIPMUX=0")
sendCMD_waitRespLine2("AT+CIPSTART=\"UDP\",\"0.0.0.0\",5000,5000,2")



############################################
#
#  Traitement données centrale innertielle
#
############################################

ic2 = I2C(0, sda=Pin(8), scl=Pin(9), freq=400000)
imu = MPU6050(ic2)

spi = SPI(1, baudrate=20000000, polarity = 0, phase=0, sck = Pin(10), mosi=Pin(11), miso=Pin(12))
Relay = Pin(26, Pin.OUT) #connecter sur CN5

g = 9.81
epsilon = 1e-1
deltaTus = 1
nbValPourMoyenne = 4
nbValPourVitesse = 10
acc = [[], [], []]
accMoyenne = [[], [], []]
T_ticks = []
T_s = []
vit = []


tft = TFT(spi,14,15,13)
tft.initg()
tft.rgb(True)

tft.fill(TFT.WHITE)
tft.text((10,10), "Activation", TFT.BLACK, sysfont, 2, nowrap=True)
tft.text((10,30), "   Vanne", TFT.BLACK, sysfont, 2, nowrap=True)
tft.text((10,50), "==========", TFT.BLACK, sysfont, 2, nowrap=True)


def moyenne(liste):
    listeMoy = [ 0 for _ in range(len(liste))]
    nbValListe = len(liste[0]) #Normalement = nbValPourMoyenne

    for k in range(nbValListe):
        for l in range(len(liste)):
            listeMoy[l] += round(liste[l][k]/nbValListe, 2)

    return listeMoy
   
   
def accMoy(listAccMoy):
    for l in range(len(listAccMoy)):
        accMoyenne[l].append(listAccMoy[l])


def viderAcc():
    for k in range(len(acc)):
        acc[k].clear()


def viderAccMoyenne():
    for k in range(len(accMoyenne)):
        accMoyenne[k].clear()
  
  
def tpsTicksToSec():
    TenSec = []
    for k in range(len(T_ticks)-1):
        TenSec.append(utime.ticks_diff(T_ticks[k+1], T_ticks[k])*1e-6)
    return TenSec


def vitesse():
    v = [0, 0, 0]
    nbValAccMoy= len(accMoyenne[0])
    cstX, cstY, cstZ = -accMoyenne[0][0], -accMoyenne[1][0], -accMoyenne[2][0] #- car v(0) = cst donc v = at - v(0)

    for k in range(nbValAccMoy-1): #normalement cst d'intégration nulles car pas de pesanteur, intégration méthode trapèzes
        v[0] += (accMoyenne[0][k] + accMoyenne[0][k+1] + 2*cstX)/2 * T_s[k]
        v[1] += (accMoyenne[1][k] + accMoyenne[1][k+1] + 2*cstY)/2 * T_s[k]
        v[2] += (accMoyenne[2][k] + accMoyenne[2][k+1] + 2*cstZ)/2 * T_s[k]
    
    for l in range(len(v)):
        v[l] = round(v[l], 3)

    return v


#Programme en continu

while True:
    
    T_ticks = []
    for i in range(nbValPourVitesse):
        for j in range(nbValPourMoyenne):
            Ax = round(imu.accel.x*g,2)
            Ay = round(imu.accel.y*g,2)
            Az = round(imu.accel.z*g,2)
            acc[0].append(Ax)
            acc[1].append(Ay)
            acc[2].append(Az)
            utime.sleep_us(deltaTus)
            
        accMoy(moyenne(acc))
        T_ticks.append(utime.ticks_us())
        
        viderAcc()
        
    
    T_s = tpsTicksToSec()
    vit = vitesse()
    
    print("vitesse moyenne {} m/s".format(vit))
    print("Temps écoulé {:.5f}s".format(utime.ticks_diff(T_ticks[-1], T_ticks[0])*1e-6))
    
    textStr = strSend()
    textLen= str(len(textStr)+10)
    Dt = "AT+CIPSEND="+textLen+"\r\n"
    uart.write(Dt)
    uart.write(textStr)
    sendCMD_waitRespLine3("AT+CIPSTART=\"UDP\",\"0.0.0.0\",5000,5000,2")
    
    viderAccMoyenne()


    tft.fillrect((0, 80),(127, 127), TFT.WHITE)
    if (abs(vit[0]) < epsilon):
        #Relay.value(1) #OFF
        tft.text((10,80), " Non", TFT.RED, sysfont, 4, nowrap=True)
    else:
        tft.text((10,80), " Oui", TFT.RED, sysfont, 4, nowrap=True)
        #Relay.value(0) #ON


    
    
    #utime.sleep_ms(1)
    
    
    

    
    
    


