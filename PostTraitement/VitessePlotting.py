import matplotlib.pyplot as plt
import numpy as np

filename="log_20-06-2022--14h29m23.txt"

fichier = open(filename, "r")
lignes = fichier.readlines()
fichier.close()

VitesseX = [0]
Temps = [0]

for ligne in lignes:
    if (ligne[0]=='V'):
        V = ligne[10:-2].strip().split(',')
        for i in range(len(V)):
            V[i] = float(V[i])
        
        VitesseX.append(V[0])

    if (ligne[0]=='T'):
        T = ligne[6:-2].strip().split(',')
        for i in range(len(T)):
            T[i] = float(T[i])
        Temps.append(round(Temps[-1] + np.array(T).sum(), 3))

plt.figure(0)
plt.plot(Temps, VitesseX)
plt.show()

    