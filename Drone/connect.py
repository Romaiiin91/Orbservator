import os
import utime
import machine



            
#Start of main program. Print system and art info


fichier = open("sortieConnect.txt", 'w')

print(os.uname())

uart = machine.UART(0)
print(uart)

print(b'A'.decode())

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
def sendCMD_waitRespLine(cmd, timeout=2000):
    print("CMD: " + cmd)
    fichier.write("CMD: {}\n".format(cmd))
    cmd +="\r\n"
    uart.write(cmd)
    waitRespLine(timeout)
    print()
    
# Walt for response with timeout

def waitRespLine(timeout=4000):
    prvMills = utime.ticks_ms()
    texte = " "
    while ((utime.ticks_ms() - prvMills) < timeout):
        if uart.any():
            fichier.write(uart.readline())
            #print("En cours")


#Get version number and turn echo OFF

sendCMD_waitRespLine("AT+GMR")
sendCMD_waitRespLine("ATEO")


#Connect to local wi-fi router
sendCMD_waitRespLine("AT+CWMODE=1")
sendCMD_waitRespLine("AT+CWJAP=\"iPhone de Romain\",\"12345678\"", timeout=10000)

sendCMD_waitRespLine("AT+CIFSR")
sendCMD_waitRespLine("AT+PING=\"www.bbc.co.uk\"",timeout=10000)

print()
print("Over")
fichier.close()

fichier = open("sortieConnect.txt", 'r')
lignes = fichier.readlines()
fichier.close()

for ligne in lignes:
    print(ligne)


