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

# print(f"La media muestral es de: {Media_Muestral_X(z_alfa_2, L)}") ## Comenntar esto para velocidad

## Aca falta estimar la tasa real de uso del canal TODO

## ==========================================================================
## Ejercicio 2

import numpy as np
import matplotlib.pyplot as plt


intervalos = 18

expon = [exponencial(0.5) for i in range(10000)]




def simular_experimento(lamb, mu, t_inicial, Nsim=10000):
    neventos = 0
    datos_simulados = []

    while neventos < Nsim:
        res = simular_canal(lamb=lamb, mu=1, t_inicial=t_inicial)
        neventos += res[0]
        datos_simulados.extend(res[4])

    while neventos > Nsim:
        datos_simulados.pop() # Saco el ultimo elemento
        neventos -= 1
    assert(len(datos_simulados) == Nsim)

    return datos_simulados




# Nsim son la cantidad de paquetes a simular
datos_simulados = simular_experimento(lamb=0.5, mu=1, t_inicial=0, Nsim=10000)


# exit()

plt.subplot(211)
n_exp, bins_exp, patch_exp = plt.hist(x=expon, bins=18, density=True)

# print(n_exp)
# print(bins_exp)
# print(patch_exp)
# print("Expon es ", expon)



plt.subplot(212)
n_sim, bins_sim, patch_sim = plt.hist(x=datos_simulados, bins=18, color="red")
# plt.show()

# print(n_sim)
# print(bins_sim)
# print(patch_sim)


## ==========================================================================
## Ejercicio 3


## Chi-cuadrado

def arreglar_arreglo_chi(arr):
    idx_menor_5 = False
    for i in range(len(arr)):
        # print(arr[i])
        if arr[i] <= 5:
            idx_menor_5 = i
            break

    # print(arr)
    # print(idx_menor_5)

    tmp = 0
    for i in range(idx_menor_5, intervalos):
        tmp += arr[i]

    # print("Before", arr)
    arr[idx_menor_5] = tmp
    arr = arr[:idx_menor_5+1]
    # print("After ", arr)s


    cutted_bins = []
    for i in range(idx_menor_5):
        cutted_bins.append([bins_sim[i], bins_sim[i+1]])
    cutted_bins.append([bins_sim[idx_menor_5], float("inf")])


    assert(len(arr) == len(cutted_bins))
    # print("LEN ARR", len(arr))
    # print("LEN Cutted", len(cutted_bins))
    return arr, cutted_bins, len(arr)


count_sim = np.histogram(datos_simulados, 18)[0]
count_sim = list(count_sim)

tt = arreglar_arreglo_chi(count_sim)

frecuencias = tt[0]
segmentos = tt[1]
largo = tt[2]

# print(largo)
N = sum(frecuencias)

## Arreglar arreglo exponenciales para obtener la probabilidad de los intervalos

count_exp = np.histogram(expon, bins_sim)[0] ## Obtener el arreglo de frecuencias en los mismos intervalos
count_exp = list(count_exp)

# Juntar las probabilidades del ultimo intervalo de n-1 a inf


def arreglar_arreglo_probabilidades_chi(count_exp, largo):

    tmp = sum(count_exp[largo-1:])
    count_exp[largo-1] = tmp

    # Eliminar los ultimos elementos
    for i in range(len(count_exp), largo, -1):
        del count_exp[i-1]

    return count_exp

N_exp = sum(count_exp)
count_exp = arreglar_arreglo_probabilidades_chi(count_exp, largo)

# print(count_exp)
# print(frecuencias)


prob = []
assert(len(count_exp) == len(frecuencias))
for i in range(largo):
    prob.append(count_exp[i]/N_exp)




## Calculo estadistico T
T = 0
for i in range(largo):
    T += ((frecuencias[i] - N * prob[i])**2 / (N * prob[i]))


from scipy.stats import chi2

# p-valor igual a una chi-cuadrado de k = 16 - 1 - 1 = 14

## p-valor = P(X^(14) > T)

# print(T)

# print(f"p-valor con chi2 de grado 14: {1-chi2.cdf(T, largo-1-1):.5f}") # n-1=2
print(f"{1-chi2.cdf(T, largo-1-1):.5f}") # n-1=2



## Ejercicio 4


from random import gammavariate
from math import exp

def Gamma_AR(k, mu):
    while True:
        u = 1 - random()
        y = -log(u) * (k * mu) # Generamos la Exponencial de parámetro 1/k*mu
        v = random()
        if v < (y/(k*mu)) ** (k-1) * exp((k-1)*(mu*k-y)/(mu*k)):
            return y


gammas = [gammavariate(0.1, 10) for _ in range(10000)]

fig, ax = plt.subplots(3)
ax[0].hist(gammas, bins=18)

# Uso el método de aceptacion y rechazo para poder generar con alfa = 0.5 , beta = 2




gammas_AR = [Gamma_AR(1, 1) for _ in range(10000)]

ax[1].hist(gammas_AR, bins=18)


ax[1].hist(datos_simulados, bins=18, color='red', alpha=0.5)
ax[2].hist(datos_simulados, bins=18, color='green', alpha=1)

# plt.show()


