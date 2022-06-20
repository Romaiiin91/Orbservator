import socket
import time

ip = "172.20.10.11"
port = 5000
txtRecu =" "
fichier = open("./log_"+time.strftime("%d-%m-%Y--%Hh%Mm%S")+".txt", "w")


# Create socket for server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
print("Do Ctrl+c to exit the program !!")

# Let's send data through UDP protocol
for _ in range(20):
    send_data = "all?"
    s.sendto(send_data.encode('utf-8'), (ip, port))

    data, address = s.recvfrom(4096)
    txtRecu = data.decode('utf-8')
    listeLignes = txtRecu.split("\n")

    print(listeLignes[-2])
    fichier.write(listeLignes[-2]+"\n")


    for ligne in listeLignes[1:-4]:
        print(ligne)
        fichier.write(ligne+"\n")
    fichier.write("\n")


# close the socket and file
s.close()
fichier.close()