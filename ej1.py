# Ejercicio 1. C se toma = 1, mu = 1 y lamb = 0.5

from random import random, seed
from math import gamma, sqrt, log

import numpy as np
import matplotlib.pyplot as plt

seed(0) # Fijar la semilla para debuggear

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
    return NT, Eventos


def exponencial(lamda):
    U = 1-random()
    return -log(U)/lamda


def simular_canal(lamb=0.5, mu=1, t_inicial=0):
    T = t_inicial + 1000 # Genera todos los eventos en los siguientes 100 tiempos
    neventos, canal = Poisson_homogeneo(lamb=lamb, T=T, mu=mu, t_inicial=t_inicial)

    print("AHHHHHHHHH",canal[-1], neventos)
    ultimo_tiempo = canal[-1][0]

    # print(f"neventos es {neventos}")
    # print(f"canal es {canal}")

    # for i in range(len(canal)):
        # print(canal[i][0], canal[i][1], canal[i][0] + canal[i][1])

    paquetes_enviados = 0
    tiempo_actual = 0
    encolados = 0

    buffer = []
    tiempos_salida = []
    tiempos_demora = []
    tiempo_espera_cola = []

    while tiempo_actual <= T:
        if len(buffer) > 0: # Tengo algo en el buffer
            tiempos_demora.append(buffer[0][1] + tiempo_actual - buffer[0][0])
            tiempo_espera_cola.append(tiempo_actual - buffer[0][0])
            tiempo_actual += (buffer[0][1])
            tiempos_salida.append(tiempo_actual)
            paquetes_enviados += 1
            buffer.pop(0)

        else: # El buffer esta vacio

            if len(canal) > 0: # El canal tiene algun paquete

                if tiempo_actual > canal[0][0]: # Me pasé algún paquete que tengo que encolar
                    buffer.append(canal[0])
                    canal.pop(0)
                    encolados += 1

                else: # El buffer esta vacio y no perdí ningún paquete. Atiendo el paquete
                    tiempo_actual = canal[0][0] + canal[0][1]
                    paquetes_enviados += 1
                    tiempos_salida.append(canal[0][0] + canal[0][1])
                    tiempos_demora.append(canal[0][1])
                    tiempo_espera_cola.append(0) # El paquete no espero nada
                    canal.pop(0)

            else: # El canal esta vacio. Simulo nuevos paquetes
                # nuevaIter = Poisson_homogeneo(lamb=lamb, T=tiempo_actual+100, mu=1, t_inicial=tiempo_actual)
                # neventos += nuevaIter[0]
                # for i in nuevaIter[1]:
                #     canal.append(i)
                # ultimo_tiempo = canal[-1][0]
                print("Me quede sin paquetes")
                break

    return paquetes_enviados, tiempo_actual, tiempos_salida, encolados, tiempos_demora, tiempo_espera_cola


def revisar_simular_canal(res):
    tmp = 0
    for i in res[2]:
        if tmp > i:
            raise ValueError('Los tiempos de salida se solapan')
        tmp = i
    return True


def simular_tiempos_demora(lamb, mu, t_inicial, Nsim=10000):
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


res = simular_canal(lamb=0.5, mu=1)

# print(f"\nPaquetes enviados {res[0]}\n tiempo_actual {res[1]}\n tiempos_salida {res[2]}\n encolados {res[3]}\n tiempo_demora {res[4]}\n tiempo_espera_cola{res[5]}\n")

# assert(revisar_simular_canal(res))

# Ejercicio 1a

# 2.33 es el z_alfa_2 para 98%

z_alfa_2 = 2.33
L = 0.01


def Media_Muestral_X(z_alfa_2, L, lamb): #z_alfa_2 = z_(alfa/2)
    tiempos_demora, buffer_tiempo_demora, tiempo_espera_cola = [], [], []
    t_inicial = 0
    'Confianza = (1 - alfa)%, amplitud del intervalo: L'

    tmp = simular_canal(lamb=lamb, mu=1, t_inicial=0)

    t_inicial = tmp[1]
    buffer_tiempo_demora = tmp[4]
    tiempo_espera_cola = tmp[5]

    X = buffer_tiempo_demora.pop(0)
    tiempos_demora.append(X)
    Media = X


    d = L / (2 * z_alfa_2)
    Scuad, n = 0, 1
    while n <= 100 or sqrt(Scuad / n) > d:
        n += 1
        if len(buffer_tiempo_demora) == 0:
            tmp = simular_canal(lamb=lamb, mu=1, t_inicial=t_inicial)
            t_inicial += tmp[1]
            buffer_tiempo_demora = tmp[4]
            tiempo_espera_cola.extend(tmp[5])

        X = buffer_tiempo_demora.pop(0)
        tiempos_demora.append(X)

        Media_Ant = Media
        Media = Media_Ant + (X - Media_Ant) / n
        Scuad = Scuad * (1 - 1 /(n-1)) + n*(Media - Media_Ant)**2
    return Media, n, Scuad, tiempos_demora, tiempo_espera_cola

import pickle

# Valores para no volver a correr la funcion
with open ('tiempos_demora_sim', 'rb') as fp:
    tiempos_demora_sim = pickle.load(fp)

with open ('tiempos_espera_cola_sim', 'rb') as fp:
    tiempos_espera_cola_sim = pickle.load(fp)


Media_Muestral_al_98 = 1.9979837101936286
n_sim = 858567
scuad = 3.9536833670037024

# resultados_simulacion = Media_Muestral_X(z_alfa_2, L, lamb=0.5)

# Media_Muestral_al_98 = resultados_simulacion[0]
# n_datos_sim = resultados_simulacion[1]
# scuad = resultados_simulacion[2]
# tiempos_demora_sim = resultados_simulacion[3]
# tiempos_espera_cola_sim = resultados_simulacion[4]

print(f"La media muestral es de: {Media_Muestral_al_98}")
print(f"La cantidad de valores generados es de: {n_sim}")
print(f"El valor de Scuad es : {scuad}")
# print(f"Los valores generados son: {result[2]}")
# Comentar esto para velocidad

# Aca falta estimar la tasa real de uso del canal TODO


# La media muestral es de: 1.9979837101936286
# La cantidad de valores generados es de: 858567




# with open('tiempos_demora_sim', 'wb') as fp:
#     pickle.dump(tiempos_demora_sim, fp)


# with open('tiempos_espera_cola_sim', 'wb') as fp:
#     pickle.dump(tiempos_espera_cola_sim, fp)



# ==========================================================================
# Ejercicio 2


# Voy a tomar 18 intervalos
intervalos = 18

expon = [exponencial(0.5) for i in range(n_sim)]


datos_simulados = tiempos_demora_sim

plt.subplot(211)
n_exp, bins_exp, patch_exp = plt.hist(x=expon, bins=18,)

# print(n_exp)
# print(bins_exp)
# print(patch_exp)
# print("Expon es ", expon)


plt.subplot(212)
n_sim_hist, bins_sim_hist, patch_sim_hist = plt.hist(x=datos_simulados, bins=18, color="red")

# plt.show()

# print(n_sim)
# print(bins_sim)
# print(patch_sim)

plt.hist(x=expon, bins=18, color='blue')
plt.hist(x=datos_simulados, bins=18, color="yellow", alpha=0.5)
# plt.show()

# ==========================================================================
# Ejercicio 3


# Chi-cuadrado

# Funcion para conseguir que todos los intervalos tengan por lo menos 5 observaciones
def arreglar_arreglo_chi_5elem(arr, bins_sim):

    idx_menor_5 = False
    for i in range(len(arr)):
        # print(arr[i])
        if arr[i] <= 5:
            idx_menor_5 = i
            break


    tmp = 0
    for i in range(idx_menor_5, intervalos):
        tmp += arr[i]

    arr[idx_menor_5] = tmp
    arr = arr[:idx_menor_5+1]


    cutted_bins = []
    for i in range(idx_menor_5):
        cutted_bins.append([bins_sim[i], bins_sim[i+1]])
    cutted_bins.append([bins_sim[idx_menor_5], float("inf")])


    assert(len(arr) == len(cutted_bins))
    # print("LEN ARR", len(arr))
    # print("LEN Cutted", len(cutted_bins))
    return arr, cutted_bins


def arreglar_arreglo_probabilidades_exp(count_exp, largo):

    # Recortar arreglo probabilidades teoricas
    tmp = sum(count_exp[largo-1:])
    count_exp[largo-1] = tmp

    # Eliminar los ultimos elementos
    for i in range(len(count_exp), largo, -1):
        del count_exp[i-1]

    return count_exp


def simulacion_ej3(datos_simulados, expon):


    count_sim = np.histogram(datos_simulados, 18)[0]
    count_sim = list(count_sim)

    print(count_sim)

    tt = arreglar_arreglo_chi_5elem(count_sim, bins_sim_hist)

    frecuencias = tt[0]
    largo = len(tt[0])
    segmentos = tt[1]

    N = sum(frecuencias)

    # Arreglar arreglo exponenciales para obtener la probabilidad de los intervalos

    count_exp = np.histogram(expon, bins_sim_hist)[0] # Obtener el arreglo de frecuencias en los mismos intervalos
    count_exp = list(count_exp)

    # Juntar las probabilidades del ultimo intervalo de n-1 a inf

    N_exp = sum(count_exp)
    count_exp = arreglar_arreglo_probabilidades_exp(count_exp, largo)


    prob = []
    assert(len(count_exp) == len(frecuencias))
    for i in range(len(count_exp)):
        prob.append(count_exp[i]/N_exp)


    # Calculo estadistico T
    T = 0
    for i in range(largo):
        # print(T)
        if (prob[i]) != 0: # Reviso que el intervalo tomado no tenga ningun valor
            T += ((frecuencias[i] - N * prob[i])**2 / (N * prob[i]))


    from scipy.stats import chi2

    # p-valor igual a una chi-cuadrado de k = 16 - 1 - 1 = 14

    # p-valor = P(X^(14) > T)

    print(T)

    # print(f"p-valor con chi2 de grado 14: {1-chi2.cdf(T, largo-1-1):.5f}") # n-1=2
    p_valor = 1-chi2.cdf(T, largo-1-1)
    # print(f"{p_valor:.5f}") # n-1=2

    return p_valor

p_valor = simulacion_ej3(datos_simulados, expon)
# print(p_valor)
print(f'{p_valor.tolist():.5f}')


# Resultado : 0.00004

# Para un nivel de confianza del 99 %
# la hipotesis nula se rechaza porque 0.01 > (p-valor=0.00004)
# Por lo tanto, la muestra simulada no proviene de una exponencial de parametro lambda=0.5

# ==================================================================================================
# Ejercicio 4


from random import gammavariate
from math import exp

def Gamma_AR(k, mu):
    while True:
        u = 1 - random()
        y = -log(u) * (k * mu) # Generamos la Exponencial de parámetro 1/k*mu
        v = random()
        if v < (y/(k*mu)) ** (k-1) * exp((k-1)*(mu*k-y)/(mu*k)):
            return y


# Estimacion Media_Tc

tc = sum(tiempos_espera_cola_sim)
n_tc = len(tiempos_espera_cola_sim)

estimacion_tc = tc/n_tc

print(estimacion_tc)


## Generacion con Gammas


gammas = [gammavariate(0.5, 2) for _ in range(n_sim)]

fig, ax = plt.subplots(4)
ax[0].hist(gammas, bins=18, color='cyan')

# Uso el método de aceptacion y rechazo para poder generar con
# alfa = 0.5, beta = 2


gammas_AR = [Gamma_AR(0.5, 2) for _ in range(n_sim)]

ax[1].hist(gammas_AR, bins=18, color='yellow')


ax[2].hist(gammas, bins=18, color='red', alpha=1)
ax[2].hist(gammas_AR, bins=18, color='blue', alpha=0.5)
rr = ax[3].hist(tiempos_espera_cola_sim, bins=18, color='green', alpha=1)


plt.show()




def calcular_chi2(datos_simulados, distrib_teo, bin_sim_hist):


    count_sim = np.histogram(datos_simulados, 18)[0]
    count_sim = list(count_sim)

    print(count_sim)

    tt = arreglar_arreglo_chi_5elem(count_sim, bins_sim_hist)


    frecuencias = tt[0]

    print("frecuencias", frecuencias)
    largo = len(tt[0])
    segmentos = tt[1]

    N = sum(frecuencias)

    # Arreglar arreglo exponenciales para obtener la probabilidad de los intervalos

    count_exp = np.histogram(expon, bins_sim_hist)[0] # Obtener el arreglo de frecuencias en los mismos intervalos
    count_exp = list(count_exp)

    # Juntar las probabilidades del ultimo intervalo de n-1 a inf

    N_exp = sum(count_exp)
    count_exp = arreglar_arreglo_probabilidades_exp(count_exp, largo)

    print("count_exp", count_exp)


    prob = []
    assert(len(count_exp) == len(frecuencias))
    for i in range(len(count_exp)):
        prob.append(count_exp[i]/N_exp)


    # Calculo estadistico T
    T = 0
    for i in range(largo):
        # print(T)
        if (prob[i]) != 0: # Reviso que el intervalo tomado no tenga ningun valor
            T += ((frecuencias[i] - N * prob[i])**2 / (N * prob[i]))


    from scipy.stats import chi2

    # p-valor igual a una chi-cuadrado de k = 16 - 1 - 1 = 14

    # p-valor = P(X^(14) > T)

    print(T)

    # print(f"p-valor con chi2 de grado 14: {1-chi2.cdf(T, largo-1-1):.5f}") # n-1=2
    p_valor = 1-chi2.cdf(T, largo-1-1)
    # print(f"{p_valor:.5f}") # n-1=2

    return p_valor

cola_espera_bins = np.histogram(tiempos_espera_cola_sim, bins=18)[0]
print(calcular_chi2(tiempos_espera_cola_sim, gammas, cola_espera_bins))


# ==================================================================================================
# Ejercicio 5


nueva_sim_1 = simular_tiempos_demora(lamb=0.05, mu=0.1, t_inicial=0, Nsim=10000)

print(nueva_sim_1)

nueva_sim_2 = simular_tiempos_demora(lamb=0.05, mu=0.1, t_inicial=0, Nsim=10000)

print(nueva_sim_2)


# plt.ylabel("Frecuencia")
# plt.xlabel("Intervalo")
# plt.title("Simulacion para lamb=0.05, mu=0.1, Nsim=10000")
# plt.subplot(121)
# plt.hist(nueva_sim_1, bins=18, color='green')


# plt.ylabel("Frecuencia")
# plt.xlabel("Intervalo")
# plt.title("Simulacion para lamb=0.05, mu=0.1, Nsim=10000")
# plt.subplot(122)
# plt.hist(nueva_sim_2, bins=18, color='green')


fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax1.title.set_text('First Plot')
ax2.title.set_text('Second Plot')

ax1.hist(nueva_sim_1, bins=18, color='green')
ax2.hist(nueva_sim_2, bins=18, color='green')

ax1.set_ylabel("Frecuencia")
ax1.set_xlabel("Intervalos")
ax1.set_title("Simulacion para lamb=0.5, mu=1, Nsim=10000")

ax2.set_ylabel("Frecuencia")
ax2.set_xlabel("Intervalos")
ax2.set_title("Simulacion para lamb=0.05, mu=0.1, Nsim=10000")

plt.show()

fig = plt.figure()
plt.hist(nueva_sim_1, bins=18, color='red')
plt.hist(nueva_sim_2, bins=18, color='green', alpha=0.5)

plt.show()