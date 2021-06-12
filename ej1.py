## Ejercicio 1. C se toma = 1, mu = 1 y lamb = 0.5

from random import random, seed
from math import sqrt, log



# seed(0) ## Fijar la semilla para debuggear

def Poisson_homogeneo(lamb, T, mu, t_inicial=0):
    t_inicial = 0
    NT = 0
    Eventos = []
    while t_inicial < T:
        U = 1 - random()
        t_inicial += -log(U)/lamb
        if t_inicial <= T:
            NT += 1
            Eventos.append((t_inicial, exponencial(mu)))
    return NT, Eventos, Eventos[-1]


def exponencial(lamda):
    U = 1-random()
    return -log(U)/lamda

# print(exponencial(1))


def simular_canal(lamb=0.5, mu=1, t_inicial=0):
    T = t_inicial + 1000 ## Esto esta haciendo ruido
    neventos, canal, ultimo_tiempo = Poisson_homogeneo(lamb=lamb, T=T, mu=1, t_inicial=0)

    ultimo_tiempo = ultimo_tiempo[0]

    # print(f"neventos es {neventos}")
    # print(f"canal es {canal}")

    # for i in range(len(canal)):
    #     print(canal[i][0], canal[i][1], canal[i][0] + canal[i][1])

    paquetes_enviados = 0
    tiempo_actual = 0
    encolados = 0

    buffer = []
    tiempos_salida = []
    tiempos_espera = []

    while tiempo_actual <= ultimo_tiempo:
        if len(buffer) > 0: ## Tengo algo en el buffer
            tiempos_espera.append(buffer[0][1] + tiempo_actual - buffer[0][0])
            tiempo_actual += (buffer[0][1])
            tiempos_salida.append(tiempo_actual)
            paquetes_enviados += 1
            buffer.pop(0)

        else: ## El buffer esta vacio

            if len(canal) > 0: ## El canal tiene algun paquete

                if tiempo_actual > canal[0][0]: ## Me pasé algún paquete que tengo que encolar
                    buffer.append(canal[0])
                    canal.pop(0)
                    encolados += 1

                else: ## El buffer esta vacio y no perdí ningún paquete. Atiendo el paquete
                    tiempo_actual = canal[0][0] + canal[0][1]
                    paquetes_enviados += 1
                    tiempos_salida.append(canal[0][0] + canal[0][1])
                    tiempos_espera.append(canal[0][1])
                    canal.pop(0)

            else: ## El canal esta vacio. Simulo nuevos paquetes
                nuevaIter = Poisson_homogeneo(lamb=lamb, T=ultimo_tiempo+10, mu=1, t_inicial=ultimo_tiempo)
                neventos += nuevaIter[0]
                for i in nuevaIter[1]:
                    canal.append(i)
                ultimo_tiempo = nuevaIter[2][0]

    return paquetes_enviados, tiempo_actual, tiempos_salida, encolados, tiempos_espera


def revisar_simular_canal(res):
    tmp = 0
    for i in res[2]:
        if tmp > i:
            raise ValueError('Los tiempos de salida se solapan')
        tmp = i
    return True



res = simular_canal(lamb=0.5, mu=1)

# print(f"\nPaquetes enviados {res[0]}\n tiempo_actual {res[1]}\n tiempos_salida {res[2]}\n encolados {res[3]}\n tiempo_espera {res[4]}\n")

assert(revisar_simular_canal(res))

## Ejercicio 1a

## 2.33 es el z_alfa_2 para 98%

z_alfa_2 = 2.33
L = 0.01


## copiado


# Nsim = 0
# pvalor = 0
# while Nsim <= 100 or sqrt(1/Nsim) > d:
#     Nsim += 1
#     uniformes= np.random.uniform(0, 1, n) # usamos uniformes porque conocemos los parámetros
#     uniformes.sort()
#     d_j = 0
#     for j in range(n):
#         u_j = uniformes[j]
#         d_j = max(d_j, (j+1)/ n-u_j, u_j-j/n)
#     if d_j >= D:
#         pvalor += 1

# print(f"{n}\t {D:.5f}\t {pvalor/Nsim:.5f}\t {Nsim}")
# if n == 100:
#     plt.hist(muestra, histtype='bar')

def Media_Muestral_X(z_alfa_2, L): #z_alfa_2 = z_(alfa/2)
    'Confianza = (1 - alfa)%, amplitud del intervalo: L'
    buffer = simular_canal(lamb=0.5, mu=1, t_inicial=0)[4]
    d = L / (2 * z_alfa_2)
    Media = buffer.pop(0)
    Scuad, n = 0, 1
    while n <= 100000 or sqrt(Scuad / n) > d:
        n += 1
        if len(buffer) == 0:
            buffer = simular_canal(lamb=0.5, mu=1, t_inicial=0)[4]
        X = buffer.pop(0)
        Media_Ant = Media
        Media = Media_Ant + (X - Media_Ant) / n
        Scuad = Scuad * (1 - 1 /(n-1)) + n*(Media - Media_Ant)**2
    return Media

print(f"La media muestral es de: {Media_Muestral_X(z_alfa_2, L)}")

## Aca falta estimar la tasa real de uso del canal

## Ejercicio 2

import numpy as np
import matplotlib.pyplot as plt


intervalos = 18

expon = [exponencial(0.5) for i in range(10000)]

normaa = []
lamb = 0.5
ultimo_tiempo = 0
t_inicial = 0
mu = 1
neventos = 0
while neventos <= 10000:
    res = simular_canal(lamb=lamb, mu=1, t_inicial=t_inicial)
    neventos += res[0]
    normaa.extend(res[4])




# expon.sort()
# expon_min = min(expon)
# expon_max = max(expon)

# bins = np.linspace(expon_min, expon_max, num=18)


plt.subplot(211)
n, bins, patch = plt.hist(x=expon, bins=18, density=True)

# print(n)
# print(bins)
# print(patch)
# print("Expon es ", expon)



plt.subplot(212)
n, bins, patch = plt.hist(x=normaa, bins=18, density=True, color="red")
plt.show()

