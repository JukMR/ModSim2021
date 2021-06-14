# Ejercicio 1. C se toma = 1, mu = 1 y lamb = 0.5

from hashlib import new
from random import random, seed
from math import gamma, sqrt, log

import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import chi2


seed(0) # Fijar la semilla para obtener resultados consistentes

def Poisson_homogeneo(lamb, mu, t_inicial=0, Npaquetes=10):
    NT = 0
    Eventos = []
    while NT < Npaquetes:
        U = 1 - random()
        t_inicial += -log(U)/lamb
        NT += 1
        Eventos.append((t_inicial, exponencial(mu)))
    return NT, Eventos


def exponencial(lamda):
    U = 1-random()
    return -log(U)/lamda


def simular_canal(lamb=0.5, mu=1, t_inicial=0, Npaquetes=100):
    neventos, canal = Poisson_homogeneo(lamb=lamb, mu=mu, t_inicial=t_inicial, Npaquetes=Npaquetes)

    paquetes_enviados = 0
    tiempo_actual = t_inicial
    encolados = 0

    buffer = []
    tiempos_salida = []
    tiempos_demora = []
    tiempo_espera_cola = []

    while paquetes_enviados < Npaquetes:
        if len(buffer) > 0: # Tengo algo en el buffer.
            llegada_paquete, ancho_paquete = buffer[0]

            tiempos_demora.append(ancho_paquete + tiempo_actual - llegada_paquete)
            tiempo_espera_cola.append(tiempo_actual - llegada_paquete)
            tiempo_actual += (ancho_paquete)
            tiempos_salida.append(tiempo_actual)
            paquetes_enviados += 1
            buffer.pop(0)

        else: # El buffer esta vacio

            if len(canal) > 0: # El canal tiene algun paquete

                llegada_paquete, ancho_paquete = canal[0]
                if tiempo_actual > llegada_paquete: # Me pasé algún paquete que tengo que encolar.
                    buffer.append((llegada_paquete, ancho_paquete))
                    canal.pop(0)
                    encolados += 1

                else: # El buffer esta vacio y no perdí ningún paquete. Atiendo el paquete.

                    llegada_paquete, ancho_paquete = canal[0]
                    tiempo_actual = llegada_paquete + ancho_paquete
                    paquetes_enviados += 1
                    tiempos_salida.append(llegada_paquete + ancho_paquete)
                    tiempos_demora.append(ancho_paquete)
                    tiempo_espera_cola.append(0) # El paquete no espero nada
                    canal.pop(0)

            else: # El canal esta vacio. Termino.
                print("Me quede sin paquetes")
                break

    return paquetes_enviados, tiempo_actual, tiempos_salida, encolados, tiempos_demora, tiempo_espera_cola


# ==========================================================================
# Ejercicio 1

# 2.33 es el z_alfa_2 para 98%

z_alfa_2 = 2.33
L = 0.01


def Media_Muestral_X(z_alfa_2, L, lamb): #z_alfa_2 = z_(alfa/2)
    tiempos_demora, buffer_tiempo_demora, tiempo_espera_cola = [], [], []
    t_inicial = 0
    'Confianza = (1 - alfa)%, amplitud del intervalo: L'

    tmp = simular_canal(lamb=lamb, mu=1, t_inicial=0, Npaquetes=1000)

    t_inicial = tmp[1]
    buffer_tiempo_demora = tmp[4]
    tiempo_espera_cola = tmp[5]

    X = buffer_tiempo_demora.pop(0)
    tiempos_demora.append(X)
    Media = X


    d = L / (2 * z_alfa_2)
    Scuad, paq_gen = 0, 1
    while paq_gen <= 100 or sqrt(Scuad / paq_gen) > d:
        paq_gen += 1
        if len(buffer_tiempo_demora) == 0:
            tmp = simular_canal(lamb=lamb, mu=1, t_inicial=t_inicial, Npaquetes=1000)
            t_inicial = tmp[1]
            buffer_tiempo_demora = tmp[4]
            tiempo_espera_cola.extend(tmp[5])

        X = buffer_tiempo_demora.pop(0)
        tiempos_demora.append(X)

        Media_Ant = Media
        Media = Media_Ant + (X - Media_Ant) / paq_gen
        Scuad = Scuad * (1 - 1 /(paq_gen-1)) + paq_gen*(Media - Media_Ant)**2
    return Media, paq_gen, Scuad, tiempos_demora, tiempo_espera_cola, t_inicial


Media_Muestral_al_98,\
    n_sim,\
    scuad,\
    tiempos_demora_sim,\
    tiempos_espera_cola_sim,\
    tiempo_total_sim\
    = Media_Muestral_X(z_alfa_2, L, lamb=0.5)

print(f"El tiempo medio de demora tau_m es de: {Media_Muestral_al_98}")
print(f"Nsim es: {n_sim}")
print(f"El tiempo total simulado es de: {tiempo_total_sim}")

# Estimacion de la tasa real de uso del canal
tasa_uso = n_sim * Media_Muestral_al_98 / tiempo_total_sim

print(f"La tasa real de uso estimada es de {tasa_uso * 100} %")

# Cálculo del intervalo de confianza al 98% de semiancho L=0.01
print(f"El intervalo de confianza del 98% es de: {Media_Muestral_al_98 - 2.33 * sqrt(scuad / n_sim)} , {Media_Muestral_al_98 + 2.33 * sqrt(scuad / n_sim)}")



# ==========================================================================
# Ejercicio 2


# Voy a tomar 18 intervalos
intervalos = 18

# El m
expon = [exponencial(0.5) for i in range(n_sim)]

plt.subplot(211)
plt.title("Histogramas de Nsim tiempos con datos simulados y Nsim datos de exponencial")
plt.hist(x=expon, bins=18, label='Datos exponencial teorica', color='blue')
plt.legend(loc='best')


plt.subplot(212)
plt.hist(x=tiempos_demora_sim, bins=18, color="red", label='Datos simulados')
plt.legend(loc='best')

plt.show()

n_exp, bins_exp, patch_exp = plt.hist(x=tiempos_demora_sim, bins=18, color="blue", label="Datos simulados", alpha=1)
plt.hist(x=expon, bins=bins_exp, color='red', label="Exponencial teorica", alpha=0.5)
plt.title("Superposicion histogramas exponencial lamb=0.5 vs tiempos de demora")
plt.legend(loc='best')
plt.show()

# ==========================================================================
# Ejercicio 3


# Test de bondad de ajuste usando Chi-cuadrado

# Función para conseguir que todos los intervalos tengan por lo menos 5
# observaciones
def arreglar_arreglo_chi_5elem(arr, bins_sim):
    idx_menor_5 = False
    for i in range(len(arr)):
        if arr[i] < 5:
            idx_menor_5 = i -1
            break

    # Todos los intervalos tienen al menos 5 elementos
    # Corrijo el ultimo intervalo para que vaya hasta infinito y termino
    if idx_menor_5 == False:
        new_bins = bins_sim
        new_bins[-1] = float('inf')
        return arr, new_bins


    # Acumular las frecuencias desde el n con menos de 5 observaciones hasta el
    # ultimo intervalo
    tmp = 0
    for i in range(idx_menor_5, len(bins_sim) - 1):
        tmp += arr[i]


    # Recortar el arreglo y guardar las frecuencias acumuladas del n con menos
    # de 5 obs. hasta el ultimo intervalo
    arr[idx_menor_5] = tmp
    arr = arr[:idx_menor_5+1]

    new_bins = bins_sim[:idx_menor_5+2]
    new_bins[-1] = float('inf')
    assert(len(arr) == len(new_bins) - 1)

    return arr, new_bins



def calcular_chi2(datos_simulados, distrib_teo):

    frec_sim, bins = np.histogram(datos_simulados, 18)
    frec_sim = list(frec_sim)

    frecuencias, segmentos = arreglar_arreglo_chi_5elem(frec_sim, bins)

    largo = len(frecuencias)

    # El arreglo de intervalos tiene que tener un elemento mas que el arreglo de
    # frecuencias
    assert(len(segmentos) - 1 == largo)

    N = sum(frecuencias)

    # Arreglar arreglo exponenciales para obtener la probabilidad de los
    # intervalos

    # Obtener el arreglo de frecuencias en los mismos intervalos
    frec_teorica = np.histogram(distrib_teo, segmentos)[0]
    frec_teorica = list(frec_teorica)

    # Juntar las probabilidades del ultimo intervalo de n-1 a inf

    N_exp = sum(frec_teorica)


    # La cantidad de intervalos tiene que ser igual para los datos teoricos y
    # los datos simulados.
    assert(len(frec_teorica) == len(frecuencias))

    prob = []
    for i in range(len(frec_teorica)):
        prob.append(frec_teorica[i]/N_exp)


    # Calculo estadistico T
    T = 0
    for i in range(largo):
        # Reviso que el intervalo tomado no tenga ningun valor con prob=0 para
        # no dividir por 0
        if (prob[i]) != 0:
            T += ((frecuencias[i] - N * prob[i])**2 / (N * prob[i]))


    # Como estamos estimando un parámetro debo tomar una chi-cuadrado con k-1-1
    # grados de libertad (con k igual al numero de intervalos cortado por la
    # funcion arreglar_arreglo_chi_5elem)


    p_valor = 1-chi2.cdf(T, largo-1-1)

    return p_valor



p_valor = calcular_chi2(tiempos_demora_sim, expon)

print(f"El p-valor del ejercicio 3 es: {p_valor}")


# Para un nivel de confianza del 99 %
# la hipotesis nula se rechaza porque 0.01 > (p-valor=0)
# Por lo tanto, la muestra simulada no proviene de una exponencial de parametro lambda=0.5

# ==================================================================================================
# Ejercicio 4


from random import gammavariate
from math import exp


# Estimacion Media_Tc

tc = sum(tiempos_espera_cola_sim)
n_tc = len(tiempos_espera_cola_sim)

estimacion_tc = tc/n_tc

print(f"La estimacion de tc es {estimacion_tc}")


## Generación con Gammas

gammas = [gammavariate(0.5, 2) for _ in range(n_sim)]


frec, bin, _ = plt.hist(tiempos_espera_cola_sim, bins=18, color='blue', alpha=1, label='tiempo cola espera')


plt.hist(gammas, bins=bin, color='orange', label="Distribucion gamma variate", alpha=0.5)
plt.title("Superposicion de histogramas gamma(0.5,2) y tiempos espera en cola simulados")
plt.legend(loc='best')
plt.show()


print(f"El p-valor del ejercicio 4 es: {calcular_chi2(tiempos_espera_cola_sim, gammas)}")


# ==================================================================================================
# Ejercicio 5


nueva_sim_1 = simular_canal(lamb=0.5, mu=1, t_inicial=0, Npaquetes=10000)[4]

nueva_sim_2 = simular_canal(lamb=0.05, mu=0.1, t_inicial=0, Npaquetes=10000)[4]


fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax1.title.set_text('First Plot')
ax2.title.set_text('Second Plot')

ax1.hist(nueva_sim_1, bins=18, color='green')
ax2.hist(nueva_sim_2, bins=18, color='green')

ax1.set_ylabel("Frecuencia")
ax1.set_xlabel("Segundos")
ax1.set_title("Simulacion para lamb=0.5, mu=1, Nsim=10000")

ax2.set_ylabel("Frecuencia")
ax2.set_xlabel("Segundos")
ax2.set_title("Simulacion para lamb=0.05, mu=0.1, Nsim=10000")

plt.show()

fig = plt.figure()
plt.hist(nueva_sim_1, bins=18, color='red', label='lamb=0.5, mu*c = 1')
plt.hist(nueva_sim_2, bins=18, color='green', alpha=0.5, label="lamb=0.05, mu*c = 0.1")
plt.legend(loc='best')
plt.title("Superposicion de los histogramas")

plt.show()



# ==================================================================================================
'''
## Anexo

# Algoritmo para encontrar los mejores parámetros de gamma

for k in range(1,11):
    print(f"alfa es {k * 0.1}, beta es {1/(k * 0.1)}")


    gammas = [gammavariate(k * 0.1, 1/(k * 0.1) ) for _ in range(n_sim)]



    # plt.hist(gammas, bins=18, color='purple', label='Gamma variate')
    # plt.legend(loc='best')
    # plt.title("Datos distribucion gamma generada")
    # plt.show()


    frec, bin, _ = plt.hist(tiempos_espera_cola_sim, bins=18, color='blue', alpha=1, label='tiempo cola espera')
    plt.hist(gammas, bins=bin, color='orange', label="Distribucion gamma variate", alpha=0.5)
    plt.legend(loc='best')
    plt.show()

'''