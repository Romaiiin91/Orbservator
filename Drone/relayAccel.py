from imu import MPU6050
import utime
from machine import Pin, I2C, SPI
from ST7735 import TFT
from sysfont import sysfont


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
T = []

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

def vitesse():
    v = [0, 0, 0]
    nbValAccMoy= len(accMoyenne[0])
    cstX, cstY, cstZ = -accMoyenne[0][0], -accMoyenne[1][0], -accMoyenne[2][0] #- car v(0) = cst donc v = at - v(0)

    for k in range(nbValAccMoy-1): #normalement cst d'intégration nulles car pas de pesanteur, intégration méthode trapèzes
        v[0] += (accMoyenne[0][k] + accMoyenne[0][k+1] + 2*cstX)/2 * utime.ticks_diff(T[k+1], T[k])*1e-6
        v[1] += (accMoyenne[1][k] + accMoyenne[1][k+1] + 2*cstY)/2 * utime.ticks_diff(T[k+1], T[k])*1e-6
        v[2] += (accMoyenne[2][k] + accMoyenne[2][k+1] + 2*cstZ)/2 * utime.ticks_diff(T[k+1], T[k])*1e-6

    return v


while True:
    T = []
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
        T.append(utime.ticks_us())
        viderAcc()
        #print("Acceleration moyenne {}".format(accMoyenne))
    #print("T ", len(T), "AccMoy ", len(accMoyenne[0])) 
    
    vit = vitesse()
    print("vitesse moyenne {} m/s".format(vit))
    print("Temps écoulé {:.2f}s".format(utime.ticks_diff(T[-1], T[0])*1e-6))
    viderAccMoyenne()


    tft.fillrect((0, 80),(127, 127), TFT.WHITE)
    if (abs(vit[0]) < epsilon):
        #Relay.value(1) #OFF
        tft.text((10,80), " Non", TFT.RED, sysfont, 4, nowrap=True)
    else:
        tft.text((10,80), " Oui", TFT.RED, sysfont, 4, nowrap=True)
        #Relay.value(0) #ON


    
    
    #utime.sleep_ms(1)
    
    
    

    
    
    

