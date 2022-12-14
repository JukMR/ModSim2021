# EJERCICIO 1
# Merida Renny, Julian

# C se toma = 1, mu = 1 y lamb = 0.5

from random import random, seed
from math import sqrt, log

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

        else: # El buffer está vacio.

            if len(canal) > 0: # El canal tiene algún paquete.

                llegada_paquete, ancho_paquete = canal[0]
                if tiempo_actual > llegada_paquete: # Me pasé algún paquete que tengo que encolar.
                    buffer.append((llegada_paquete, ancho_paquete))
                    canal.pop(0)
                    encolados += 1

                else: # El buffer está vacio y no perdí ningún paquete. Atiendo el paquete.

                    llegada_paquete, ancho_paquete = canal[0]
                    tiempo_actual = llegada_paquete + ancho_paquete
                    paquetes_enviados += 1
                    tiempos_salida.append(llegada_paquete + ancho_paquete)
                    tiempos_demora.append(ancho_paquete)
                    tiempo_espera_cola.append(0) # El paquete no esperó nada.
                    canal.pop(0)

            else: # El canal está vacio. Termino.
                print("Me quedé sin paquetes")
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

# Estimación de la tasa real de uso del canal
tasa_uso = n_sim / tiempo_total_sim

print(f"La tasa real de uso estimada es de {tasa_uso * 100} %")


# Cálculo del intervalo de confianza al 98% de semiancho L=0.01
print(f"El intervalo de confianza del 98% es de: {Media_Muestral_al_98 - 2.33 * sqrt(scuad / n_sim)} , {Media_Muestral_al_98 + 2.33 * sqrt(scuad / n_sim)}")



# ==========================================================================
# Ejercicio 2


# Voy a tomar 18 intervalos.
intervalos = 18

# Genero los datos para la hipotesis nula de que los datos simulados
# corresponden a esta distribución
expon = [exponencial(0.5) for i in range(n_sim)]

plt.subplot(211)
plt.title("Histograma de Nsim tiempos datos simulados y datos exponenciales")
frec, bin, _ = plt.hist(x=tiempos_demora_sim, bins=18, color="blue", label='Tiempos demora simulados', edgecolor='black')
plt.xlabel("Tiempo")
plt.ylabel("Frecuencia")
plt.legend(loc='best')

plt.subplot(212)
plt.hist(x=expon, bins=bin, label='Datos de exponencial(0.5)', color='red', edgecolor='black')
plt.xlabel("Tiempo")
plt.ylabel("Frecuencia")
plt.legend(loc='best')

plt.savefig(fname='histogramas_separados_sim_exp.png')
plt.show()




plt.hist(x=[tiempos_demora_sim, expon], bins=bin, color=['blue', 'red'], label=["Tiempos demora simulados", "Datos de exponencial(0.5)"], edgecolor='black')
plt.title("Comparación histogramas exponencial λ=0.5 vs tiempos de demora")
plt.xlabel("Tiempo")
plt.ylabel("Frecuencia")
plt.legend(loc='best')
plt.savefig(fname="comparacion_hist_sim_exp.png")
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



def calcular_chi2(datos_simulados, distrib_teo, parametros_estimados):

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


    print(f"El estadístico T es igual a {T}")
    p_valor = 1-chi2.cdf(T, largo-1-1)

    return p_valor


# El parametro que estamos estimando es el lambda 0.5 de la exponencial
p_valor = calcular_chi2(tiempos_demora_sim, expon, parametros_estimados=1)

print(f"El p-valor del ejercicio 3 es: {p_valor}")


# Para un nivel de confianza del 99 %
# la hipotesis nula se rechaza porque 0.01 > (p-valor=0)
# Por lo tanto, la muestra simulada no proviene de una exponencial de parametro lambda=0.5

# ==================================================================================================
# Ejercicio 4


from random import gammavariate


# Estimacion Media_Tc

tc = sum(tiempos_espera_cola_sim)
n_tc = len(tiempos_espera_cola_sim)

estimacion_tc = tc/n_tc

print(f"La estimación de tc es {estimacion_tc}")


## Generación con Gammas

gammas = [gammavariate(0.5, 2) for _ in range(n_sim)]


plt.hist(x=[tiempos_espera_cola_sim, gammas], bins=18, color=['orange', 'cyan'], label=['Tiempos de cola espera', 'Distribución Gamma(0.5,2)'], edgecolor='black')


plt.title("Comparación Gamma y Tiempos de espera en cola simulados")
plt.xlabel("Tiempo")
plt.ylabel("Frecuencias")
plt.legend(loc='best')
plt.savefig(fname="hist_gamma_vs_sim.png")
plt.show()


# Los parametros estimados son alpha=0.5 y beta=2
print(f"El p-valor del ejercicio 4 es: {calcular_chi2(tiempos_espera_cola_sim, gammas, parametros_estimados=2)}")


# ==================================================================================================
# Ejercicio 5


# Ahora C es 0.1. Entonces mu*c = 1, entonces mu = 10

nueva_sim_1 = simular_canal(lamb=0.5, mu=10, t_inicial=0, Npaquetes=10000)[4]

# Ahora C es 0.1. Entonces mu*c = 0.1, entonces mu = 1


nueva_sim_2 = simular_canal(lamb=0.05, mu=1, t_inicial=0, Npaquetes=10000)[4]


fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ax1.hist(nueva_sim_1, bins=18, color='green', edgecolor='black', label='λ=0.5, μ*C=1')
ax1.legend(loc='best')
ax2.hist(nueva_sim_2, bins=18, color='yellow', edgecolor='black', label='λ=0.05, μ*C=0.1')
ax2.legend(loc='best')

ax1.set_ylabel("Frecuencia")
ax1.set_xlabel("Tiempo")

ax2.set_ylabel("Frecuencia")
ax2.set_xlabel("Tiempo")

plt.legend(loc='best')
fig.suptitle('Tiempos de demora con distintos parámetros con Nsim=10000')

plt.savefig(fname='sim1_sim2.png')
plt.show()

fig = plt.figure()
plt.hist(x=[nueva_sim_1, nueva_sim_2], bins=18, color=['green', 'yellow'], label=['λ=0.5, μ*C = 1', 'λ=0.05, μ*C = 0.1'], edgecolor='black')
plt.legend(loc='best')
plt.xlabel("Tiempos de demora")
plt.ylabel("Frecuencias")

plt.title("Comparación de histogramas tiempos demora con distintos parámetros")

plt.savefig(fname='comparacion_sim1_sim2')
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


    frec, bin, _ = plt.hist(x=[tiempos_espera_cola_sim, gammas], bins=18, color=['blue', 'orange'], label=['tiempo cola espera', 'Distribucion gamma variate'])
    plt.legend(loc='best')
    plt.show()

'''








# -------------------------------------------------------------------# EJERCICIO 2
# Merida Renny, Julian

from random import random, seed
from math import log, ceil

seed(0) ## Fijar la semilla para debuggear

def Poisson_homogeneo(lamb, T):
    t = 0
    NT = 0
    Eventos = []
    while t < T:
        U = 1 - random()
        t += -log(U)/lamb
        if t <= T:
            NT += 1
            Eventos.append(t)
    return NT, Eventos



def simular_canal_aloha(lamb=0.5, T=10):
    neventos, canal = Poisson_homogeneo(lamb, T)

    n_paquetes_rotos= 0
    t_actual = 0
    paquetes_enviados = []
    paquetes_rotos = []

    while t_actual < T:
        if len(canal) > 1:

            # El tiempo actual es menor al tiempo del proximo paquete
            if t_actual <= canal[0]:

                # Revisar que tengo tiempo suficiente para mandar el paquete
                if canal[0] + 1 < canal[1]: #
                    t_actual = canal[0] + 1
                    paquetes_enviados.append(canal[0] + 1)
                    canal.pop(0)

                # No tengo tiempo para mandar el paquete, se rompe
                else:
                    paquetes_rotos.append(canal[0] + 1)
                    t_actual = canal[0] + 1
                    n_paquetes_rotos += 1
                    canal.pop(0)

            # El tiempo actual es mayor al del paquete. Esto quiere decir que el paquete ya colapsó.
            else:
                t_actual = canal[0] + 1
                paquetes_rotos.append(canal[0] + 1)
                canal.pop(0)
                n_paquetes_rotos += 1

        # El canal tiene 1 o 0 paquetes. No puedo comparar entre paquetes
        else:
            # El canal tiene 1 paquete
            if len(canal) == 1:
                # Tengo tiempo para enviar el ultimo paquete
                if canal[0] + 1 < T:
                        t_actual = canal[0] + 1
                        paquetes_enviados.append(canal[0] + 1)
                        canal.pop(0)

                # No tengo tiempo para encolar el ultimo paquete
                else:
                    # print("Termine simulacion")
                    break

            # El canal está vacio
            else:
                # print("Termine simulacion")
                break

    return paquetes_enviados, paquetes_rotos,  n_paquetes_rotos, len(paquetes_enviados), neventos



res = simular_canal_aloha(lamb=0.5, T=20)



# Para este algoritmos los paquetes entran al canal en el momento ti. Si se
# generaron entre un t(i-1) y t(i) entonces "esperaran" hasta t(i) para entrar
# al canal

def simular_canal_aloha_ranurado(lamb=0.5, T=10):
    neventos, canal = Poisson_homogeneo(lamb, T)

    n_paquetes_rotos = 0
    t_actual = 0
    paquetes_enviados = []
    paquetes_rotos = []

    while t_actual < T:

        # Tengo al menos dos elementos para comparar en el canal
        if len(canal) > 1:

            # No me quedaron paquetes colapsados
            if t_actual < ceil(canal[0]):

                # Tengo tiempo para enviar el paquete
                if ceil(canal[0]) < ceil(canal[1]):
                    paquetes_enviados.append(ceil(canal[0]) + 1)
                    t_actual = ceil(canal[0])
                    canal.pop(0)

                # No tengo tiempo para enviar el paquete, se rompe
                else:
                    paquetes_rotos.append(ceil(canal[0]) + 1)
                    n_paquetes_rotos += 1
                    t_actual = ceil(canal[0])
                    canal.pop(0)

            # El paquete en el que estoy está roto
            else:
                paquetes_rotos.append(ceil(canal[0]) + 1)
                n_paquetes_rotos += 1
                canal.pop(0)

        # Me queda menos de 2 elementos en el canal
        else:

            # Me queda 1 elemento en el canal
            if len(canal) == 1:

                # Tengo tiempo para enviarlo
                if ceil(canal[0]) + 1 < T:
                    paquetes_enviados.append(ceil(canal[0]) + 1)
                    t_actual = ceil(canal[0]) + 1
                    canal.pop(0)

                # No tengo tiempo para enviarlo
                else:
                    break

            # No me quedan paquetes en el canal
            else:
                break


    return paquetes_enviados, paquetes_rotos,  n_paquetes_rotos, len(paquetes_enviados), neventos


res = simular_canal_aloha_ranurado(lamb=1, T=20)


# print(f"La tasa de uso es {res[3] / 20 * 100} %")

## Todas las simulaciones se harán simulando T=10000

# ==================================================================
# Ejercicio a

def tasa_uso_puro(lamb, T):
    tiempo_uso = simular_canal_aloha(lamb=lamb, T=T)[3]
    return tiempo_uso/T * 100

def tasa_uso_ranurado(lamb, T):
    tiempo_uso = simular_canal_aloha_ranurado(lamb=lamb, T=T)[3]
    return tiempo_uso/T * 100


def ejercicio1(f, string):
    for k in range(1, 31):
        print(f"{string} : {f(0.1 * k, 10000):.2f} % para lamb = {0.1 * k:.2f}")


ejercicio1(tasa_uso_puro, "tasa_uso_puro")
ejercicio1(tasa_uso_ranurado, "tasa_uso_ranurado")

# ==================================================================
# Ejercicio b

def prob_paquete_puro(lamb, T):
    _, _, _, cant_paquetes_enviados, neventos = simular_canal_aloha(lamb=lamb, T=T)
    return cant_paquetes_enviados / neventos

def prob_paquete_ranurado(lamb, T):
    _, _, _, cant_paquetes_enviados, neventos = simular_canal_aloha_ranurado(lamb=lamb, T=T)
    return cant_paquetes_enviados / neventos

def ejercicio2(f, string):
    for k in range(1, 31):
        print(f"{string} : p = {f(0.1 * k, 10000):.2f} para lamb = {0.1 * k:.2f}")


ejercicio2(prob_paquete_puro, "prob_paquete_puro")
ejercicio2(prob_paquete_ranurado, "prob_paquete_ranurado")


# ==================================================================
# Ejercicio c

def ejercicio3(f, string):
    tasas, lambs  = [], []
    for k in range(1, 31):
        lamb = 0.1 * k
        Nsim = 10000

        lambs.append(lamb)
        tasas.append(f(lamb, Nsim)) # guardar tasa en un arreglo

        # print(f"{string} : {tasas[-1]:.2f} % para lamb = {lamb:.2f}")

    maximo = max(tasas)
    lamb_max = lambs[tasas.index(maximo)]

    return maximo, lamb_max

print(ejercicio3(tasa_uso_puro, "tasa_uso_puro"))
print(ejercicio3(tasa_uso_ranurado, "tasa_uso_ranurado"))

# ==================================================================
# Ejercicio d




tasas_uso_puro = [tasa_uso_puro(0.1 * k, T=10000) for k in range(1,31)]
tasas_uso_ranurado = [tasa_uso_ranurado(0.1 * k, T=10000) for k in range(1,31)]

lambs = [0.1 * k for k in range(1,31)]

# print(tasas_uso_puro)
# print(tasas_uso_ranurado)
# print(lambs)

import matplotlib.pyplot as plt

plt.title("Comparación tasas de uso versus distintos λ")
plt.plot(lambs, tasas_uso_puro, marker='o', color='blue', label="Aloha puro")
plt.xlabel("Lambda")
plt.ylabel("Tasa uso")

plt.plot(lambs, tasas_uso_ranurado, marker='o', color='red', label="Aloha Ranurado")
plt.legend(loc='best')
plt.savefig(fname="ej2_histograma_lambdas")
plt.show()

