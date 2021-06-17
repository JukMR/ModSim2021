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
plt.xlabel("Lambdas")
plt.ylabel("Tasas uso")

plt.plot(lambs, tasas_uso_ranurado, marker='o', color='red', label="Aloha Ranurado")
plt.legend(loc='best')
plt.savefig(fname="ej2_histograma_lambdas")
plt.show()

